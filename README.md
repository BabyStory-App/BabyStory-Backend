# babystory_backend

babystory 백엔드 레포지토리입니다.

> 201904008 곽재원.

### 폴더 내용

- apis: Router.

- model: 데이터베이스 모델.(sqlalchemy)

  - types: 데이터베이스 모델의 타입(Pydantic)

- schemas: Router에서 input/output으로 사용되는 값의 타입.

  - 예를 들어 baby, cry, parent로 메인 라우터 주소가 존재할 경우 baby, cry, parent의 스키마 파일을 생성, 관리

- services: 비즈니스 로직

#### 지금 단계에서 사용되지는 않는 것.

- assets: 프로젝트에서 사용되는 파일

  - 이미지

  - 딥러닝 모델

  - 음성 파일

- auth: 보안 로직 관련(손 댈 필요가 없을 것)

- constants: 상수(변하지 않는 값)

  - 프로젝트 경로

  - 도메인 이름.

- core: 프로젝트에 종속되는 중요한 로직

  - env: 암호화 환경 변수

- dataset: 데이터셋(대충 사용된 데이터 저장한 것)

- log: 로그 값.

  - 에러 로그

  - 아기 울음 분석 로그

- utils: 유틸리티 함수(프로젝트에 종속되지 않는 함수)
