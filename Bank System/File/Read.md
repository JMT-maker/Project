# 🏦 통합 계좌 관리 시스템 (Integrated Bank Management System)

파이썬을 활용하여 설계된 레이어드 아키텍처(Layered Architecture) 기반의 금융 계좌 관리 시스템입니다.
사용자 중심의 뱅킹 서비스와 관리자 모드를 통한 강력한 데이터 제어 기능을 제공합니다.

# 🚀 주요 기능 (Key Features)
1. 사용자 서비스 (User Services)계좌 관리: 5대 주요 은행(하나, 우리, 국민, 신한, 기업) 계좌 생성, 조회 및 별칭 설정.
   금융 거래: 입금, 출금, 계좌이체 및 상세 거래 내역 조회 기능.검색 필터: 계좌번호, 별칭, 은행별 다각도 필터링 지원.
2. 관리자 기능 (Admin Mode)별도 인증을 통한 관리자 권한 진입.전체 사용자 정보 조회, 수정 및 삭제 권한.
3. 시스템 안정성 (System Integrity)트랜잭션 원자성: 이체 과정 중 오류 발생 시 자동 롤백을 수행하여 자산 손실 방지.
   데이터 검증: 최초 입금액(1,000원 이상) 제한 및 잔액 초과 이체 차단.

# 🏗 시스템 아키텍처 (Architecture)
유지보수성 극대화를 위해 시스템을 세 가지 계층으로 분리하여 설계했습니다.


UI Layer: 콘솔 입출력 및 사용자 메뉴 인터페이스 담당.


Service Layer: 이체 원자성 처리 및 비즈니스 로직 검증.


Data Layer: User, Account, Transaction 객체 관리 및 데이터 영속성 처리.   

## 📊데이터베이스 설계 (ER Diagram)초기 3개 테이블 구성에서 거래 내역 추적의 한계를 극복하기 위해 
TRANSACTION 테이블을 추가한 4개 테이블 구조로 고도화했습니다.
테이블,설명,주요 속성
USER,사용자 인증 및 권한 관리 ,"user_id, password, is_admin +1"
BANK,은행 목록 관리 ,"bank_code, bank_name "
ACCOUNT,계좌 정보 저장 ,"account_num, balance, alias +1"
TRANSACTION,거래 내역 기록 ,"type, amount, balance_after +2"

# 💻 핵심 로직: 이체 원자성 (Atomic Transfer)금융 데이터의 무결성을 보장하기 위해 예외 발생 시 수동 롤백을 수행하는 로직을 구현했습니다.

def transfer(from_acc, to_acc, amt):
    if amt <= 0: return False
    try:
        from_acc.withdraw(amt) # 출금
        to_acc.deposit(amt)    # 입금
    except Exception:
        from_acc.deposit(amt)  # 예외 발생 시 롤백
        print("이체 실패")


📅 프로젝트 정보

작성자: 조지민 


과정명: AISW 

제작일: 2026.04.13 ~ 2026.04.17 

🛠 향후 개선 방향
비밀번호 입력 횟수 제한 보안 강화.

이자 계산 및 환전 기능 고도화.

GUI 기반 인터페이스 개선.        
