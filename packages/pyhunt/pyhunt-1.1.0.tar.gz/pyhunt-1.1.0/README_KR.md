
<div align="center">

<img src="docs/logo.png" alt="pyhunt_logo" width="200"/>

# pyhunt

`pyhunt`는 로그를 시각적으로 표현하여 빠른 구조 파악과 디버깅을 지원하는    
경량 로깅 도구입니다. 함수에 데코레이터만 추가하면, 
모든 로그를 자동으로 추적하여 터미널에 출력합니다.

[![PyPI version](https://img.shields.io/pypi/v/pyhunt.svg)](https://pypi.org/project/pyhunt/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyhunt.svg)](https://pypi.org/project/pyhunt/)

#### [English](/README.md) | 한국어

---

https://github.com/user-attachments/assets/3d4389fe-4708-423a-812e-25f2e7200053

<img src="docs/description.png" alt="pyhunt_description" width="600"/>

</div>

## 주요 특징

- **자동 함수/메서드 호출 추적**: `@trace` 데코레이터 하나로 동기/비동기 함수, 클래스 호출 흐름을 자동 기록
- **풍부한 색상과 트리 구조 로그**: 호출 뎁스에 따른 색상 및 인덴트로 가독성 향상
- **다양한 로그 레벨 지원**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **CLI를 통한 로그 레벨 설정**: `.env` 파일에 `HUNT_LEVEL` 저장 및 관리
- **AI 워크플로우에 최적화**: AI가 생성한 코드를 손쉽게 추적할 수 있습니다.
- **예외 발생 시 상세 정보 제공**: 호출 인자, 위치, 스택트레이스 포함


## 설치 방법

### pip 을 이용해 설치
```bash
pip install pyhunt
```

### uv 를 이용해 설치
```bash
uv add pyhunt
```

## 빠른 시작

### 1. 환경변수 파일 설정
```bash
hunt
```

`.env` 파일에 `HUNT_LEVEL=DEBUG` 값이 설정됩니다.


### 2. 함수 또는 클래스에 `@trace` 적용
자세한 예제는 [examples](https://github.com/pyhunt/pyhunt/tree/main/examples) 폴더를 참고하세요.


#### 기본 예제
```py
from pyhunt import trace

@trace
def test(value):
    return value
```

#### 비동기 함수
```py
@trace
async def test(value):
    return value
```

#### 클래스
```py
@trace
class MyClass:
    def first_method(self, value):
        return value

    def second_method(self, value):
        return value
```

## AI와 함께 사용

### 룰 셋업
`.cursorrules` , `.clinerules` 또는 `.roorules` 에 아래와 같이 룰을 추가합니다.
```md
<logging-rules>

**Import:** Import the decorator with `from pyhunt import trace`.
**Tracing:** Use the `@trace` decorator to automatically log function calls and execution times.
**Avoid `print()`:** Do not use the `print()` function.
**Exception Handling:** Use `try`/`except Exception as e: raise e` blocks to maintain traceback.

</logging-rules>
```

### 기존 코드베이스 수정
**"로깅 룰에 따라 코드를 수정하세요."** 라고 명령합니다.

## Logger 사용법
`logger` 방식은 중요한 부분만 일부 사용하는것을 권장합니다.  
`@trace`를 통해 대부분의 동작이 추적되며, 과도한 사용은 가독성에 영향을 끼칠 수 있습니다.  

```py
from pyhunt import logger

logger.debug("This is a debug log.")
logger.info("This is an info log.")
logger.warning("This is a warning log.")
logger.error("This is an error log.")
logger.critical("This is a critical log.")
```


## CLI 사용법

```bash
hunt [옵션]
```

### 지원 옵션

- `--debug` : DEBUG 레벨 (가장 상세)
- `--info` : INFO 레벨
- `--warning` : WARNING 레벨
- `--error` : ERROR 레벨
- `--critical` : CRITICAL 레벨

옵션 미지정 시 기본값은 `INFO`입니다.




