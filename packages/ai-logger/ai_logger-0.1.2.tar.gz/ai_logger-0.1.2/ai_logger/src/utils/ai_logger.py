from typing import Optional, List
import functools
import json
import logging
import inspect
import traceback
import sys
import os
import time
import re
import pkgutil
import importlib
import psycopg2
from psycopg2.extras import Json
from datetime import datetime
import json as json_module  # Rename to avoid conflict
from pathlib import Path
from .models import AIEvent, ModelEvent, DataEvent, ErrorEvent
from .config import USE_DB, get_db_config

# Custom JSON encoder for datetime objects
class DateTimeEncoder(json_module.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Pydantic models for our logging structure


# Main AILogger class
class AILogger:
    def __init__(self, 
                app_name: str,
                log_file: Optional[str] = None,
                console_output: bool = True,
                log_level: int = logging.WARNING,  # Default to WARNING
                excluded_patterns: Optional[List[str]] = None,
                use_db: bool = None,
                db_name: Optional[str] = None,
                db_table: Optional[str] = None):
        """
        Initialize the AI Logger
        
        Args:
            app_name: Name of the application
            log_file: Path to the log file (if None, no file logging)
            console_output: Whether to output to console
            log_level: Logging level (default: WARNING)
            excluded_patterns: List of regex patterns for functions/classes to exclude
            use_db: Whether to store logs in database (overrides config)
            db_name: Custom database name (defaults to config)
            db_table: Custom table name for database logging (defaults to app_name)
        """
        self.app_name = app_name
        self.log_level = log_level
        self.excluded_patterns = excluded_patterns or []
        self._compiled_patterns = [re.compile(pattern) for pattern in self.excluded_patterns]
        self.log_file_path = log_file
        
        # Database configuration
        self.use_db = use_db if use_db is not None else USE_DB
        self.db_config = get_db_config() if self.use_db else None
        
        # Set custom database name if provided
        if db_name and self.db_config:
            self.db_config['dbname'] = db_name
            
        self.db_table = db_table or app_name.lower().replace(' ', '_')
        
        if self.use_db:
            self._init_database()
        
        # Event accumulator - dictionary with timestamps as keys
        self.events = {}
        
        # Set up Python logger for console output
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(log_level)
        
        # Clear any existing handlers
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
            
        # Create formatter for console output
        formatter = logging.Formatter('%(message)s')
        
        # Console handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
        # Make sure log directory exists
        if log_file:
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
                
            # If log file exists, load existing events
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        self.events = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    # If file is empty or invalid JSON, start with empty dict
                    self.events = {}
            
    def _should_exclude(self, name: str) -> bool:
        """Check if a function or class should be excluded from logging"""
        return any(pattern.search(name) for pattern in self._compiled_patterns)
    
    def _get_caller_info(self, stack_level=2):
        """Get information about the caller"""
        frame = inspect.currentframe()
        # Go up stack_level frames
        for _ in range(stack_level):
            if frame.f_back:
                frame = frame.f_back
            else:
                break
                
        file_name = frame.f_code.co_filename
        line_number = frame.f_lineno
        function_name = frame.f_code.co_name
        
        return {
            "file_name": file_name,
            "line_number": line_number,
            "function_name": function_name
        }
        
    def _create_db_if_not_exists(self):
        """Create database if it doesn't exist"""
        try:
            # Connect to default postgres database to check if our database exists
            conn = psycopg2.connect(
                dbname="postgres",
                user=self.db_config['user'],
                password=self.db_config['password'],
                host=self.db_config['host'],
                port=self.db_config['port']
            )
            conn.autocommit = True  # Enable autocommit for database creation
            cursor = conn.cursor()
            
            # Check if database exists
            cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s", (self.db_config['dbname'],))
            db_exists = cursor.fetchone()
            
            if not db_exists:
                # Database doesn't exist, create it
                cursor.execute(f"CREATE DATABASE {self.db_config['dbname']}")
                print(f"Database '{self.db_config['dbname']}' created successfully")
            else:
                print(f"Database '{self.db_config['dbname']}' already exists")
                
            # Close connection to postgres database
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error checking/creating database: {e}")
            self.use_db = False
            
    def _init_database(self):
        """Initialize database connection and create table if needed"""
        if not self.use_db:
            return
            
        try:
            # First ensure database exists
            self._create_db_if_not_exists()
            
            # Connect to our database
            self.conn = psycopg2.connect(
                dbname=self.db_config['dbname'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                host=self.db_config['host'],
                port=self.db_config['port']
            )
            self.cursor = self.conn.cursor()
            
            # Create table if it doesn't exist - PostgreSQL syntax
            self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.db_table} (
                event_id TEXT PRIMARY KEY,
                timestamp TIMESTAMP,
                event_type TEXT,
                component TEXT,
                file_name TEXT,
                line_number INTEGER,
                function_name TEXT,
                event_json JSONB
            )
            ''')
            
            # Create indexes for common query fields
            self.cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{self.db_table}_timestamp ON {self.db_table}(timestamp)")
            self.cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{self.db_table}_event_type ON {self.db_table}(event_type)")
            self.cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{self.db_table}_component ON {self.db_table}(component)")
            self.conn.commit()
            print(f"Database initialized with table: {self.db_table}")
        except Exception as e:
            print(f"Error initializing database: {e}")
            self.use_db = False
    
    def _log_to_database(self, event_dict):
        """Log event to database"""
        if not self.use_db:
            return
            
        try:
            # Prepare values for INSERT
            event_id = event_dict["event_id"]
            timestamp = event_dict["timestamp"].isoformat() if isinstance(event_dict["timestamp"], datetime) else event_dict["timestamp"]
            event_type = event_dict["event_type"]
            component = event_dict["component"]
            file_name = event_dict["file_name"]
            line_number = event_dict["line_number"]
            function_name = event_dict["function_name"]
            # First convert datetime objects to strings using our custom encoder
            serialized_dict = json_module.loads(json_module.dumps(event_dict, cls=DateTimeEncoder))
            
            # Use psycopg2's Json adapter for proper JSONB handling
            event_json = Json(serialized_dict)
            
            # Insert into database (PostgreSQL uses %s for parameters)
            self.cursor.execute(
                f"""
                INSERT INTO {self.db_table} 
                (event_id, timestamp, event_type, component, file_name, line_number, function_name, event_json)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (event_id) DO UPDATE SET 
                    timestamp = EXCLUDED.timestamp,
                    event_type = EXCLUDED.event_type,
                    component = EXCLUDED.component,
                    file_name = EXCLUDED.file_name,
                    line_number = EXCLUDED.line_number,
                    function_name = EXCLUDED.function_name,
                    event_json = EXCLUDED.event_json
                """,
                (event_id, timestamp, event_type, component, file_name, line_number, function_name, event_json)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Error logging to database: {e}")
    
    def _log_event(self, event: AIEvent):
        """
        Add event to the event dictionary and update log file
        Uses timestamp as key and event as value in the dictionary
        """
        # Add application info
        event.details.update({
            "app_name": self.app_name,
        })
        
        # Convert to dict for storage
        event_dict = event.model_dump()
        
        # Use the timestamp as the key (formatted as ISO string)
        timestamp_key = event_dict["timestamp"].isoformat()
        
        # Store the event in our dictionary
        self.events[timestamp_key] = event_dict
        
        # If this is above log level, also output to console
        if self.logger.level <= self.log_level:
            self.logger.log(self.log_level, event.model_dump_json())
        
        # Write to file if file logging is enabled
        if self.log_file_path:
            # Write the entire events dictionary to the file with indentation
            with open(self.log_file_path, 'w') as f:
                json_module.dump(self.events, f, indent=2, cls=DateTimeEncoder)
                
        # Log to database if enabled
        if self.use_db:
            self._log_to_database(event_dict)
        
    def log_model_event(self, model_name: str, event_type: str, 
                        input_tokens: Optional[int] = None,
                        output_tokens: Optional[int] = None,
                        latency_ms: Optional[float] = None,
                        **details):
        """Log a model-related event with caller info"""
        caller_info = self._get_caller_info()
        
        event = ModelEvent(
            event_type=event_type,
            component="model",
            model_name=model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            file_name=caller_info["file_name"],
            line_number=caller_info["line_number"],
            function_name=caller_info["function_name"],
            details=details
        )
        self._log_event(event)
        
    def log_data_event(self, data_source: str, event_type: str,
                      record_count: Optional[int] = None,
                      **details):
        """Log a data-related event with caller info"""
        caller_info = self._get_caller_info()
        
        event = DataEvent(
            event_type=event_type,
            component="data",
            data_source=data_source,
            record_count=record_count,
            file_name=caller_info["file_name"],
            line_number=caller_info["line_number"],
            function_name=caller_info["function_name"],
            details=details
        )
        self._log_event(event)
        
    def log_error(self, error_type: str, error_message: str,
                 component: str = "application",
                 include_traceback: bool = True,
                 severity: str = "ERROR"):
        """Log an error event with caller info"""
        caller_info = self._get_caller_info()
        
        stack_trace = None
        if include_traceback:
            stack_trace = traceback.format_exc()
            
        event = ErrorEvent(
            event_type="error",
            component=component,
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace,
            severity=severity,
            file_name=caller_info["file_name"],
            line_number=caller_info["line_number"],
            function_name=caller_info["function_name"]
        )
        self._log_event(event)
        
    def wrap_function(self, component: str = None):
        """
        Decorator to wrap functions and log their execution
        
        Args:
            component: The component name (if None, uses function module)
        """
        def decorator(func):
            # Check if function should be excluded
            if self._should_exclude(func.__name__):
                return func
                
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Get component name
                comp = component
                if comp is None:
                    comp = func.__module__ or "unknown"
                
                # Get caller info
                caller_info = self._get_caller_info(stack_level=1)
                
                # Log the start
                start_time = time.time()
                
                try:
                    # Execute the function
                    result = func(*args, **kwargs)
                    
                    # Calculate duration
                    (time.time() - start_time) * 1000
                    
                    # Return result without logging success if below ERROR level
                    return result
                    
                except Exception as e:
                    # Always log errors
                    self.log_error(
                        error_type=type(e).__name__,
                        error_message=str(e),
                        component=comp
                    )
                    raise
                    
            return wrapper
        return decorator
    
    def wrap_class(self, component: str = None):
        """
        Class decorator to wrap all methods of a class
        
        Args:
            component: The component name (if None, uses class name)
        """
        def decorator(cls):
            # Check if class should be excluded
            if self._should_exclude(cls.__name__):
                return cls
                
            comp = component
            if comp is None:
                comp = cls.__name__
                
            # Find all methods that aren't special methods
            for name, method in inspect.getmembers(cls, inspect.isfunction):
                if not name.startswith('__') and not self._should_exclude(name):
                    setattr(cls, name, self.wrap_function(comp)(method))
            return cls
        return decorator

    def wrap_all_modules(self, package_paths: List[str], exclude_modules: Optional[List[str]] = None):
        """
        Wrap all functions and classes in specified modules
        
        Args:
            package_paths: List of package paths to wrap
            exclude_modules: List of module names to exclude
        """
        exclude_modules = exclude_modules or []
        
        for package_path in package_paths:
            package = __import__(package_path, fromlist=['*'])
            for module_info in pkgutil.iter_modules([os.path.dirname(package.__file__)]):
                module_name = f"{package_path}.{module_info.name}"
                
                # Skip excluded modules
                if module_name in exclude_modules or any(self._should_exclude(name) for name in [module_name, module_info.name]):
                    continue
                
                try:
                    module = importlib.import_module(module_name)
                    
                    # Wrap all functions
                    for name, obj in inspect.getmembers(module, inspect.isfunction):
                        if obj.__module__ == module_name and not self._should_exclude(name):
                            setattr(module, name, self.wrap_function(module_name)(obj))
                    
                    # Wrap all classes
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if obj.__module__ == module_name and not self._should_exclude(name):
                            setattr(module, name, self.wrap_class(module_name)(obj))
                            
                except (ImportError, AttributeError) as e:
                    print(f"Error wrapping module {module_name}: {e}")

    def __del__(self):
        """Destructor to close database connection when logger is destroyed"""
        if hasattr(self, 'conn') and self.conn is not None:
            try:
                self.conn.close()
                print("Database connection closed")
            except:
                pass
    
    def capture_existing_loggers(self, logger_names=None, capture_all=False, min_level=None):
        """
        Redirect logs from existing loggers to this AI logger
        
        Args:
            logger_names: List of logger names to capture (e.g., ['sqlalchemy', 'uvicorn'])
            capture_all: If True, capture all loggers (use with caution!)
            min_level: Minimum level to capture (defaults to self.log_level)
        """
        if logger_names is None and not capture_all:
            logger_names = []
        
        # Use provided min_level or default to this logger's level
        capture_level = min_level if min_level is not None else self.log_level
        
        # Custom handler to redirect logs to our logger
        class AILogHandler(logging.Handler):
            def __init__(self, ai_logger, min_capture_level):
                super().__init__()
                self.ai_logger = ai_logger
                # Set the handler level to filter logs before they reach emit
                self.setLevel(min_capture_level)
                
            def emit(self, record):
                try:
                    # The handler level should filter, but double-check just in case
                    if record.levelno < self.level:
                        return
                        
                    # Map the log level to severity
                    severity_map = {
                        logging.DEBUG: "DEBUG",
                        logging.INFO: "INFO", 
                        logging.WARNING: "WARNING",
                        logging.ERROR: "ERROR",
                        logging.CRITICAL: "CRITICAL"
                    }
                    severity = severity_map.get(record.levelno, "INFO")
                    
                    # Get the log message
                    msg = self.format(record)
                    
                    # Avoid recursive logging - don't log messages from our own logger
                    if record.name == self.ai_logger.app_name:
                        return
                        
                    # Create event directly to avoid triggering more log messages
                    event = ErrorEvent(
                        event_type="error",
                        component=record.name,
                        error_type="LogMessage",
                        error_message=msg,
                        stack_trace=None,
                        severity=severity,
                        file_name=getattr(record, 'pathname', None),
                        line_number=getattr(record, 'lineno', None),
                        function_name=getattr(record, 'funcName', None),
                        details={"logger_name": record.name}
                    )
                    
                    # Add app name to details
                    event.details.update({
                        "app_name": self.ai_logger.app_name,
                    })
                    
                    # Convert to dict for storage
                    event_dict = event.model_dump()
                    
                    # Use the timestamp as the key (formatted as ISO string)
                    timestamp_key = event_dict["timestamp"].isoformat()
                    
                    # Store the event in our dictionary without triggering logging
                    self.ai_logger.events[timestamp_key] = event_dict
                    
                    # Write to file directly without going through logger
                    if self.ai_logger.log_file_path:
                        with open(self.ai_logger.log_file_path, 'w') as f:
                            json_module.dump(self.ai_logger.events, f, indent=2, cls=DateTimeEncoder)
                            
                except Exception:
                    self.handleError(record)
        
        # Create the handler instance with our capture level
        ai_handler = AILogHandler(self, capture_level)
        
        # Set formatter for the handler
        formatter = logging.Formatter('%(message)s')
        ai_handler.setFormatter(formatter)
        
        if capture_all:
            # Get the root logger to capture all logs
            root_logger = logging.getLogger()
            root_logger.addHandler(ai_handler)
            print(f"Capturing all logs at level {logging.getLevelName(capture_level)} and above")
            return
            
        # Add the handler to each specified logger
        for logger_name in logger_names:
            try:
                logger = logging.getLogger(logger_name)
                logger.addHandler(ai_handler)
                print(f"Capturing logs from '{logger_name}' at level {logging.getLevelName(capture_level)} and above")
            except Exception as e:
                print(f"Error capturing logger '{logger_name}': {e}")
                    
# Global instance and setup functions
