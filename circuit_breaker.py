"""
Circuit Breaker Pattern for LLM API Protection
3 states: CLOSED → OPEN → HALF_OPEN
"""
import asyncio
import time
import logging
from datetime import datetime
from typing import Optional, Callable, Any
from enum import Enum

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = "closed"      # Hoạt động bình thường
    OPEN = "open"          # Đã ngắt, không gọi API
    HALF_OPEN = "half_open"  # Thử nghiệm, cho 1 request


class CircuitBreaker:
    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,      # Số lần thất bại để mở
        timeout_seconds: int = 60,       # Thời gian mở circuit
        half_open_max_calls: int = 1,    # Số request thử khi half-open
        success_threshold: int = 2,      # Số lần thành công để đóng lại
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.half_open_max_calls = half_open_max_calls
        self.success_threshold = success_threshold
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.last_state_change: float = time.time()
        self.half_open_calls_made = 0
        
        # Lock cho async
        self._lock = asyncio.Lock()
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Gọi function với circuit breaker bảo vệ"""
        async with self._lock:
            # Kiểm tra state hiện tại
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    logger.info(f"[{self.name}] Circuit OPEN -> HALF_OPEN (timeout reached)")
                    self._transition_to_half_open()
                else:
                    remaining = self.timeout_seconds - (time.time() - self.last_failure_time)
                    raise Exception(f"Circuit OPEN for {self.name}, remaining: {remaining:.0f}s")
            
            if self.state == CircuitState.HALF_OPEN:
                if self.half_open_calls_made >= self.half_open_max_calls:
                    raise Exception(f"Circuit HALF_OPEN for {self.name}, max calls reached")
                self.half_open_calls_made += 1
        
        # Thực hiện call
        try:
            result = await func(*args, **kwargs)
            await self._record_success()
            return result
        except Exception as e:
            await self._record_failure()
            raise e
    
    async def _record_success(self):
        async with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.success_threshold:
                    logger.info(f"[{self.name}] Circuit HALF_OPEN -> CLOSED (recovered)")
                    self._transition_to_closed()
            else:
                self.failure_count = 0  # Reset failure count
    
    async def _record_failure(self):
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                logger.warning(f"[{self.name}] Circuit CLOSED -> OPEN (failures: {self.failure_count})")
                self._transition_to_open()
            elif self.state == CircuitState.HALF_OPEN:
                logger.warning(f"[{self.name}] Circuit HALF_OPEN -> OPEN (test failed)")
                self._transition_to_open()
    
    def _should_attempt_reset(self) -> bool:
        return (time.time() - self.last_failure_time) >= self.timeout_seconds
    
    def _transition_to_open(self):
        self.state = CircuitState.OPEN
        self.last_state_change = time.time()
        self.half_open_calls_made = 0
        self.success_count = 0
    
    def _transition_to_half_open(self):
        self.state = CircuitState.HALF_OPEN
        self.last_state_change = time.time()
        self.half_open_calls_made = 0
        self.success_count = 0
    
    def _transition_to_closed(self):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.half_open_calls_made = 0
    
    def get_state(self) -> dict:
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure": self.last_failure_time,
            "state_duration_seconds": time.time() - self.last_state_change,
        }


class CircuitBreakerRegistry:
    """Singleton registry cho toàn hệ thống"""
    _instance = None
    _circuits: dict = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._circuits = {}
        return cls._instance
    
    def get(self, name: str, **kwargs) -> CircuitBreaker:
        if name not in self._circuits:
            self._circuits[name] = CircuitBreaker(name, **kwargs)
        return self._circuits[name]
    
    def get_all_states(self) -> dict:
        return {name: cb.get_state() for name, cb in self._circuits.items()}
    
    def reset(self, name: str):
        if name in self._circuits:
            del self._circuits[name]
            logger.info(f"Reset circuit: {name}")


# Singleton instance
circuit_registry = CircuitBreakerRegistry()
