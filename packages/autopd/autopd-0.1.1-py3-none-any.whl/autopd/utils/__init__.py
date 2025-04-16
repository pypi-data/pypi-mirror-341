"""
Utility functions for AutoPipelineDoctor.
"""

import logging
import os
import json
import time
import datetime
import platform
import socket
import uuid
import sys
import subprocess
import threading
import queue
from typing import Dict, List, Optional, Any, Union, Tuple, Callable

logger = logging.getLogger(__name__)

def setup_logging(level=logging.INFO, log_file=None):
    """
    Set up logging for AutoPipelineDoctor.
    
    Args:
        level: Logging level
        log_file: Path to log file (None for console only)
    """
    # Create logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Create file handler if log_file is specified
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set up autopd logger
    autopd_logger = logging.getLogger('autopd')
    autopd_logger.setLevel(level)
    
    logger.info(f"Logging set up with level {level}")

def get_system_info():
    """
    Get system information.
    
    Returns:
        Dictionary of system information
    """
    system_info = {
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'python_implementation': platform.python_implementation(),
        'hostname': socket.gethostname(),
        'cpu_count': os.cpu_count(),
        'time': datetime.datetime.now().isoformat()
    }
    
    # Get package versions
    package_versions = {}
    
    for package in ['torch', 'numpy', 'pandas', 'matplotlib', 'transformers', 'pytorch_lightning', 'deepspeed']:
        try:
            module = importlib.import_module(package)
            package_versions[package] = getattr(module, '__version__', 'unknown')
        except ImportError:
            package_versions[package] = 'not installed'
    
    system_info['package_versions'] = package_versions
    
    return system_info

def generate_unique_id():
    """
    Generate a unique ID.
    
    Returns:
        Unique ID string
    """
    return str(uuid.uuid4())

def format_time(seconds):
    """
    Format time in seconds to a human-readable string.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.2f} hours"

def format_bytes(bytes_value):
    """
    Format bytes to a human-readable string.
    
    Args:
        bytes_value: Value in bytes
        
    Returns:
        Formatted string
    """
    if bytes_value < 1024:
        return f"{bytes_value} B"
    elif bytes_value < 1024 * 1024:
        kb = bytes_value / 1024
        return f"{kb:.2f} KB"
    elif bytes_value < 1024 * 1024 * 1024:
        mb = bytes_value / (1024 * 1024)
        return f"{mb:.2f} MB"
    else:
        gb = bytes_value / (1024 * 1024 * 1024)
        return f"{gb:.2f} GB"

def run_command(command, timeout=None):
    """
    Run a shell command and return the output.
    
    Args:
        command: Command to run
        timeout: Timeout in seconds
        
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True
        )
        
        stdout, stderr = process.communicate(timeout=timeout)
        return_code = process.returncode
        
        return return_code, stdout, stderr
    
    except subprocess.TimeoutExpired:
        process.kill()
        return -1, '', 'Command timed out'
    
    except Exception as e:
        return -1, '', str(e)

def run_async(func, *args, **kwargs):
    """
    Run a function asynchronously.
    
    Args:
        func: Function to run
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Thread object
    """
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()
    return thread

def run_with_timeout(func, timeout, *args, **kwargs):
    """
    Run a function with a timeout.
    
    Args:
        func: Function to run
        timeout: Timeout in seconds
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Function result or None if timed out
    """
    result_queue = queue.Queue()
    
    def wrapper():
        try:
            result = func(*args, **kwargs)
            result_queue.put(('result', result))
        except Exception as e:
            result_queue.put(('exception', e))
    
    thread = threading.Thread(target=wrapper)
    thread.daemon = True
    thread.start()
    
    try:
        result_type, result = result_queue.get(timeout=timeout)
        
        if result_type == 'exception':
            raise result
        
        return result
    
    except queue.Empty:
        return None

def safe_divide(a, b, default=0.0):
    """
    Safely divide two numbers, returning a default value if the denominator is zero.
    
    Args:
        a: Numerator
        b: Denominator
        default: Default value to return if b is zero
        
    Returns:
        a / b or default if b is zero
    """
    return a / b if b != 0 else default

def moving_average(values, window_size):
    """
    Calculate the moving average of a list of values.
    
    Args:
        values: List of values
        window_size: Window size
        
    Returns:
        List of moving averages
    """
    if not values or window_size <= 0:
        return []
    
    if window_size == 1:
        return values.copy()
    
    result = []
    
    for i in range(len(values)):
        window_start = max(0, i - window_size + 1)
        window = values[window_start:i+1]
        result.append(sum(window) / len(window))
    
    return result

def exponential_moving_average(values, alpha):
    """
    Calculate the exponential moving average of a list of values.
    
    Args:
        values: List of values
        alpha: Smoothing factor (0 < alpha <= 1)
        
    Returns:
        List of exponential moving averages
    """
    if not values or alpha <= 0 or alpha > 1:
        return []
    
    result = [values[0]]
    
    for i in range(1, len(values)):
        result.append(alpha * values[i] + (1 - alpha) * result[i-1])
    
    return result

def detect_anomalies(values, window_size=10, threshold=2.0):
    """
    Detect anomalies in a list of values using z-score.
    
    Args:
        values: List of values
        window_size: Window size for calculating mean and standard deviation
        threshold: Z-score threshold for anomaly detection
        
    Returns:
        List of indices of anomalous values
    """
    if not values or window_size <= 0:
        return []
    
    import numpy as np
    
    anomalies = []
    
    for i in range(len(values)):
        window_start = max(0, i - window_size)
        window = values[window_start:i]
        
        if len(window) >= 2:
            mean = np.mean(window)
            std = np.std(window)
            
            if std > 0:
                z_score = abs(values[i] - mean) / std
                
                if z_score > threshold:
                    anomalies.append(i)
    
    return anomalies

def save_json(data, file_path):
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        file_path: Path to save the data to
        
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
    
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {e}")
        return False

def load_json(file_path):
    """
    Load data from a JSON file.
    
    Args:
        file_path: Path to load the data from
        
    Returns:
        Loaded data or None if an error occurred
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    
    except Exception as e:
        logger.error(f"Error loading JSON from {file_path}: {e}")
        return None

def is_notebook():
    """
    Check if the code is running in a Jupyter notebook.
    
    Returns:
        True if running in a notebook, False otherwise
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal IPython
        else:
            return False  # Other type
    except NameError:
        return False  # Standard Python interpreter

def get_available_memory():
    """
    Get available system memory.
    
    Returns:
        Available memory in bytes or None if not available
    """
    try:
        import psutil
        return psutil.virtual_memory().available
    except ImportError:
        logger.warning("psutil not installed. Cannot get available memory.")
        return None

def get_gpu_memory():
    """
    Get GPU memory information.
    
    Returns:
        Dictionary of GPU memory information or None if not available
    """
    try:
        import torch
        
        if not torch.cuda.is_available():
            return None
        
        result = {}
        
        for i in range(torch.cuda.device_count()):
            result[f'cuda:{i}'] = {
                'total': torch.cuda.get_device_properties(i).total_memory,
                'allocated': torch.cuda.memory_allocated(i),
                'reserved': torch.cuda.memory_reserved(i)
            }
        
        return result
    
    except ImportError:
        logger.warning("PyTorch not installed. Cannot get GPU memory.")
        return None

def get_cpu_info():
    """
    Get CPU information.
    
    Returns:
        Dictionary of CPU information or None if not available
    """
    try:
        import psutil
        import cpuinfo
        
        info = cpuinfo.get_cpu_info()
        
        return {
            'brand': info.get('brand_raw', 'unknown'),
            'arch': info.get('arch', 'unknown'),
            'cores': psutil.cpu_count(logical=False),
            'threads': psutil.cpu_count(logical=True),
            'frequency': psutil.cpu_freq().current if psutil.cpu_freq() else None,
            'usage': psutil.cpu_percent(interval=0.1)
        }
    
    except ImportError:
        logger.warning("psutil or cpuinfo not installed. Cannot get CPU information.")
        return None

def get_gpu_info():
    """
    Get GPU information.
    
    Returns:
        Dictionary of GPU information or None if not available
    """
    try:
        import torch
        
        if not torch.cuda.is_available():
            return None
        
        result = {}
        
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            
            result[f'cuda:{i}'] = {
                'name': props.name,
                'total_memory': props.total_memory,
                'major': props.major,
                'minor': props.minor,
                'multi_processor_count': props.multi_processor_count
            }
        
        return result
    
    except ImportError:
        logger.warning("PyTorch not installed. Cannot get GPU information.")
        return None

def get_memory_usage():
    """
    Get memory usage information.
    
    Returns:
        Dictionary of memory usage information or None if not available
    """
    try:
        import psutil
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            'rss': memory_info.rss,  # Resident Set Size
            'vms': memory_info.vms,  # Virtual Memory Size
            'percent': process.memory_percent()
        }
    
    except ImportError:
        logger.warning("psutil not installed. Cannot get memory usage.")
        return None

def get_disk_usage():
    """
    Get disk usage information.
    
    Returns:
        Dictionary of disk usage information or None if not available
    """
    try:
        import psutil
        
        usage = psutil.disk_usage('/')
        
        return {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': usage.percent
        }
    
    except ImportError:
        logger.warning("psutil not installed. Cannot get disk usage.")
        return None

def get_network_usage():
    """
    Get network usage information.
    
    Returns:
        Dictionary of network usage information or None if not available
    """
    try:
        import psutil
        
        net_io = psutil.net_io_counters()
        
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errin': net_io.errin,
            'errout': net_io.errout,
            'dropin': net_io.dropin,
            'dropout': net_io.dropout
        }
    
    except ImportError:
        logger.warning("psutil not installed. Cannot get network usage.")
        return None

def get_process_info():
    """
    Get process information.
    
    Returns:
        Dictionary of process information or None if not available
    """
    try:
        import psutil
        
        process = psutil.Process(os.getpid())
        
        return {
            'pid': process.pid,
            'name': process.name(),
            'status': process.status(),
            'create_time': process.create_time(),
            'cpu_percent': process.cpu_percent(interval=0.1),
            'memory_percent': process.memory_percent(),
            'num_threads': process.num_threads(),
            'username': process.username()
        }
    
    except ImportError:
        logger.warning("psutil not installed. Cannot get process information.")
        return None

def get_python_info():
    """
    Get Python information.
    
    Returns:
        Dictionary of Python information
    """
    return {
        'version': platform.python_version(),
        'implementation': platform.python_implementation(),
        'compiler': platform.python_compiler(),
        'build': platform.python_build(),
        'executable': sys.executable,
        'path': sys.path
    }

def get_package_versions():
    """
    Get versions of installed packages.
    
    Returns:
        Dictionary of package versions
    """
    try:
        import pkg_resources
        
        return {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    
    except ImportError:
        logger.warning("pkg_resources not available. Cannot get package versions.")
        return {}

def get_environment_variables():
    """
    Get environment variables.
    
    Returns:
        Dictionary of environment variables
    """
    return dict(os.environ)

def get_hardware_info():
    """
    Get hardware information.
    
    Returns:
        Dictionary of hardware information
    """
    info = {
        'platform': platform.platform(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'cpu_count': os.cpu_count()
    }
    
    # Add CPU info
    cpu_info = get_cpu_info()
    if cpu_info:
        info['cpu'] = cpu_info
    
    # Add GPU info
    gpu_info = get_gpu_info()
    if gpu_info:
        info['gpu'] = gpu_info
    
    # Add memory info
    try:
        import psutil
        memory = psutil.virtual_memory()
        info['memory'] = {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent
        }
    except ImportError:
        pass
    
    return info

def get_software_info():
    """
    Get software information.
    
    Returns:
        Dictionary of software information
    """
    info = {
        'os': platform.system(),
        'os_version': platform.version(),
        'os_release': platform.release(),
        'python': get_python_info()
    }
    
    # Add package versions
    package_versions = {}
    
    for package in ['torch', 'numpy', 'pandas', 'matplotlib', 'transformers', 'pytorch_lightning', 'deepspeed']:
        try:
            module = __import__(package)
            package_versions[package] = getattr(module, '__version__', 'unknown')
        except ImportError:
            package_versions[package] = 'not installed'
    
    info['packages'] = package_versions
    
    return info

def get_system_metrics():
    """
    Get system metrics.
    
    Returns:
        Dictionary of system metrics
    """
    metrics = {}
    
    # Add CPU metrics
    try:
        import psutil
        metrics['cpu'] = {
            'percent': psutil.cpu_percent(interval=0.1, percpu=True),
            'avg_percent': psutil.cpu_percent(interval=0.1)
        }
    except ImportError:
        pass
    
    # Add memory metrics
    try:
        import psutil
        memory = psutil.virtual_memory()
        metrics['memory'] = {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percent': memory.percent
        }
    except ImportError:
        pass
    
    # Add GPU metrics
    gpu_memory = get_gpu_memory()
    if gpu_memory:
        metrics['gpu_memory'] = gpu_memory
    
    # Add disk metrics
    disk_usage = get_disk_usage()
    if disk_usage:
        metrics['disk'] = disk_usage
    
    # Add network metrics
    network_usage = get_network_usage()
    if network_usage:
        metrics['network'] = network_usage
    
    return metrics

def get_all_info():
    """
    Get all system and software information.
    
    Returns:
        Dictionary of all information
    """
    return {
        'hardware': get_hardware_info(),
        'software': get_software_info(),
        'metrics': get_system_metrics(),
        'process': get_process_info(),
        'time': datetime.datetime.now().isoformat()
    }

def throttle(func, interval):
    """
    Create a throttled version of a function that can only be called once per interval.
    
    Args:
        func: Function to throttle
        interval: Minimum interval between calls in seconds
        
    Returns:
        Throttled function
    """
    last_call = [0]
    
    @wraps(func)
    def throttled(*args, **kwargs):
        current_time = time.time()
        
        if current_time - last_call[0] >= interval:
            last_call[0] = current_time
            return func(*args, **kwargs)
        
        return None
    
    return throttled

def debounce(func, wait):
    """
    Create a debounced version of a function that delays its execution until after wait seconds have elapsed since the last time it was invoked.
    
    Args:
        func: Function to debounce
        wait: Wait time in seconds
        
    Returns:
        Debounced function
    """
    timer = None
    
    @wraps(func)
    def debounced(*args, **kwargs):
        nonlocal timer
        
        def call_func():
            return func(*args, **kwargs)
        
        if timer is not None:
            timer.cancel()
        
        timer = threading.Timer(wait, call_func)
        timer.daemon = True
        timer.start()
    
    return debounced

def retry(func, max_retries=3, delay=1.0, backoff=2.0, exceptions=(Exception,)):
    """
    Create a retrying version of a function that retries on specified exceptions.
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        delay: Initial delay between retries in seconds
        backoff: Backoff multiplier
        exceptions: Tuple of exceptions to catch
        
    Returns:
        Retrying function
    """
    @wraps(func)
    def retrying(*args, **kwargs):
        retries = 0
        current_delay = delay
        
        while True:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                retries += 1
                
                if retries > max_retries:
                    raise
                
                logger.warning(f"Retry {retries}/{max_retries} after error: {e}")
                time.sleep(current_delay)
                current_delay *= backoff
    
    return retrying

def memoize(func):
    """
    Create a memoized version of a function that caches its results.
    
    Args:
        func: Function to memoize
        
    Returns:
        Memoized function
    """
    cache = {}
    
    @wraps(func)
    def memoized(*args, **kwargs):
        # Create a key from the arguments
        key = str(args) + str(sorted(kwargs.items()))
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        
        return cache[key]
    
    # Add a method to clear the cache
    memoized.clear_cache = lambda: cache.clear()
    
    return memoized

def timed(func):
    """
    Create a timed version of a function that logs its execution time.
    
    Args:
        func: Function to time
        
    Returns:
        Timed function
    """
    @wraps(func)
    def timed_func(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger.info(f"{func.__name__} took {end_time - start_time:.6f} seconds")
        
        return result
    
    return timed_func

def logged(func):
    """
    Create a logged version of a function that logs its arguments and result.
    
    Args:
        func: Function to log
        
    Returns:
        Logged function
    """
    @wraps(func)
    def logged_func(*args, **kwargs):
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} returned {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised {e}")
            raise
    
    return logged_func

def deprecated(func):
    """
    Mark a function as deprecated.
    
    Args:
        func: Function to mark as deprecated
        
    Returns:
        Deprecated function
    """
    @wraps(func)
    def deprecated_func(*args, **kwargs):
        logger.warning(f"{func.__name__} is deprecated and will be removed in a future version")
        return func(*args, **kwargs)
    
    return deprecated_func

def synchronized(func):
    """
    Create a synchronized version of a function that can only be called by one thread at a time.
    
    Args:
        func: Function to synchronize
        
    Returns:
        Synchronized function
    """
    lock = threading.RLock()
    
    @wraps(func)
    def synchronized_func(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    
    return synchronized_func

def cached_property(func):
    """
    Create a cached property that is computed only once.
    
    Args:
        func: Function to cache
        
    Returns:
        Cached property
    """
    attr_name = '_cached_' + func.__name__
    
    @property
    @wraps(func)
    def cached_func(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    
    return cached_func

def singleton(cls):
    """
    Create a singleton class that can only be instantiated once.
    
    Args:
        cls: Class to make a singleton
        
    Returns:
        Singleton class
    """
    instances = {}
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

def classproperty(func):
    """
    Create a class property that can be accessed from the class.
    
    Args:
        func: Function to make a class property
        
    Returns:
        Class property
    """
    class ClassPropertyDescriptor:
        def __init__(self, fget):
            self.fget = fget
        
        def __get__(self, obj, objtype=None):
            return self.fget(objtype)
    
    return ClassPropertyDescriptor(func)

def timeit(func=None, repeat=1):
    """
    Time the execution of a function.
    
    Args:
        func: Function to time
        repeat: Number of times to repeat the function
        
    Returns:
        Timed function or decorator
    """
    if func is None:
        return lambda f: timeit(f, repeat=repeat)
    
    @wraps(func)
    def timed_func(*args, **kwargs):
        times = []
        
        for _ in range(repeat):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            times.append(end_time - start_time)
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        logger.info(f"{func.__name__} took {avg_time:.6f} seconds on average (min: {min_time:.6f}, max: {max_time:.6f}, repeat: {repeat})")
        
        return result
    
    return timed_func

def profile(func):
    """
    Profile the execution of a function.
    
    Args:
        func: Function to profile
        
    Returns:
        Profiled function
    """
    @wraps(func)
    def profiled_func(*args, **kwargs):
        try:
            import cProfile
            import pstats
            import io
            
            pr = cProfile.Profile()
            pr.enable()
            
            result = func(*args, **kwargs)
            
            pr.disable()
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
            ps.print_stats(20)
            
            logger.info(f"Profile for {func.__name__}:\n{s.getvalue()}")
            
            return result
        
        except ImportError:
            logger.warning("cProfile not available. Cannot profile function.")
            return func(*args, **kwargs)
    
    return profiled_func

def trace(func):
    """
    Trace the execution of a function.
    
    Args:
        func: Function to trace
        
    Returns:
        Traced function
    """
    @wraps(func)
    def traced_func(*args, **kwargs):
        logger.debug(f"Entering {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Exiting {func.__name__}")
            return result
        except Exception as e:
            logger.debug(f"Exception in {func.__name__}: {e}")
            raise
    
    return traced_func

def rate_limited(max_calls, period):
    """
    Create a rate-limited version of a function that can only be called a certain number of times in a period.
    
    Args:
        max_calls: Maximum number of calls
        period: Period in seconds
        
    Returns:
        Rate-limited function
    """
    calls = []
    
    def decorator(func):
        @wraps(func)
        def rate_limited_func(*args, **kwargs):
            current_time = time.time()
            
            # Remove old calls
            while calls and calls[0] < current_time - period:
                calls.pop(0)
            
            # Check if we've reached the maximum number of calls
            if len(calls) >= max_calls:
                raise Exception(f"Rate limit exceeded: {max_calls} calls per {period} seconds")
            
            # Add current call
            calls.append(current_time)
            
            return func(*args, **kwargs)
        
        return rate_limited_func
    
    return decorator

def catch_exceptions(func):
    """
    Catch exceptions raised by a function and log them.
    
    Args:
        func: Function to catch exceptions for
        
    Returns:
        Exception-catching function
    """
    @wraps(func)
    def catching_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in {func.__name__}: {e}")
            return None
    
    return catching_func

def with_timeout(timeout):
    """
    Create a timeout version of a function that raises an exception if it takes too long.
    
    Args:
        timeout: Timeout in seconds
        
    Returns:
        Timeout function
    """
    def decorator(func):
        @wraps(func)
        def timeout_func(*args, **kwargs):
            return run_with_timeout(func, timeout, *args, **kwargs)
        
        return timeout_func
    
    return decorator

def lazy_property(func):
    """
    Create a lazy property that is computed only when accessed.
    
    Args:
        func: Function to make a lazy property
        
    Returns:
        Lazy property
    """
    attr_name = '_lazy_' + func.__name__
    
    @property
    @wraps(func)
    def lazy_func(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    
    return lazy_func

def import_optional_dependency(name, extra=""):
    """
    Import an optional dependency.
    
    Args:
        name: Name of the dependency
        extra: Extra information to include in the error message
        
    Returns:
        Imported module or None if not available
    """
    try:
        import importlib
        return importlib.import_module(name)
    except ImportError:
        if extra:
            logger.warning(f"{name} is not installed. {extra}")
        else:
            logger.warning(f"{name} is not installed.")
        return None
