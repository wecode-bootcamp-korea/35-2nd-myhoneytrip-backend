# 35-2nd-myhoneytrip-backend

## 팀원

 - BACKEND
 
 안상현, 음정민, 황유정
 
 - FRONTEND
 
 구단희, 김익현, 신수정, 이강철
 
 
 

## 개발 기간
- 개발 기간 : 2022-08-01 ~ 2022-08-12 (12일)
- 협업 툴 : Slack, Trello, Github, Notion

## 프로젝트 목표

마이리얼트립(https://www.myrealtrip.com/)을 참조한 비행 예약 사이트 구현

---

### 구현 사항

공통: ERD모델링

**안상현**
- 비행기 예약
  - 탑승객 별 비행기 예약 시스템 API구현
- 내 예약
  - 내가 예약한 비행편 조회 및 취소 API구현
  - 예약 상세 정보 조회 API구현

**음정민**
- 카카오 회원가입&로그인
   - 카카오 소셜 로그인을 이용해서 로그인과 회원가입 구현
   - 카카오 인가코드와 토큰을 이용해 닉네임, 이메일(선택)을 받아온다
   - 해당 유저가 우리 사이트 회원이 아니면 회원가입후 로그인
   - 해당 유저가 우리 사이트 회원이면 로그인
   - 로그인 후 우리 서버의 토큰을 발급한다
- 로그인 데코레이터
   
**황유정**
- 사용자 검색 결과 기반 비행스케줄 리스트 API구현 
   - 검색 결과에 따른 필터기능 및 페이지네이션 구현

---

## 사이트 시현 영상

https://user-images.githubusercontent.com/99232122/184281715-92bcc9a4-fe11-4405-9c61-a79ed58b75f0.mov

## DB모델링

<img width="1020" alt="스크린샷 2022-08-12 오후 12 50 01" src="https://user-images.githubusercontent.com/99232122/184281793-0633dd6f-21e1-4959-9f50-82abb42d9b9d.png">


## API 명세서

<img width="792" alt="스크린샷 2022-08-12 오후 12 52 04" src="https://user-images.githubusercontent.com/99232122/184281987-10aae35c-4bb9-4067-a31b-3355491115ef.png">

## 프로젝트 배포 주소

http://2nd-myhoneytrip.s3-website.ap-northeast-2.amazonaws.com/

## 기술 스택
|                                                Language                                                |                                                Framwork                                                |                                               Database                                               |                                                     ENV                                                      |                                                   HTTP                                                   |                                                  Deploy                                                 |
| :----------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------: |:------------------------------------------------------------------------------------------------------: |
| <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> | <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> | <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=black"> | <img src="https://img.shields.io/badge/miniconda3-44A833?style=for-the-badge&logo=anaconda&logoColor=white"> | <img src="https://img.shields.io/badge/postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white"> | <img src="https://img.shields.io/badge/aws-232F3E?style=for-the-badge&logo=Amazon AWS&logoColor=white">|

