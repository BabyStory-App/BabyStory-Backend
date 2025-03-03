# babystory Backend

[BabyStory App](https://github.com/BabyStory-App)의 Backend 레포지토리입니다.

AI와의 원활한 연동을 위해 백엔드는 FastAPI 프레임워크로 개발되었습니다.

전체 화면 스크린샷은 [BabyStory App Screenshots](https://github.com/BabyStory-App/.github/tree/main/assets/Screenshots)에서, 시연 영상은 [BabyStory App Demo](https://github.com/BabyStory-App/.github/tree/main/assets/Screen%20recordings)에서 확인 가능합니다.

## 개발 과정

본 프로젝트는 TDD(테스트 주도 개발) 기반의 개발 방법론을 채택하여 다음과 같은 순서로 진행되었습니다.

1. 프로젝트 요구사항 분석
2. Notion을 활용한 API 명세서 작성
3. API 명세서를 토대로 테스트 코드 작성
4. 테스트에 부합하는 실제 코드 구현
5. 구현된 코드에 대한 테스트 진행

![poster1](https://raw.githubusercontent.com/BabyStory-App/.github/refs/heads/main/assets/poster/poster.pdf7.jpg)

협업은 Notion을 통해 이루어졌으며, 코드 관리는 Github에서 Trunk-based 방식으로 관리하였습니다. 자세한 개발 방법론은 [Development Methodology](https://github.com/BabyStory-App/.github/blob/main/doc/Development%20Methodology.pdf)를 참고하시기 바랍니다.

## 데이터베이스 설계

데이터베이스는 다음과 같습니다.

![erd](https://raw.githubusercontent.com/BabyStory-App/.github/refs/heads/main/assets/erd.jpg)
