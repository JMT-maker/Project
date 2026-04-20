import datetime

# --- [데이터 저장소] ---
users = {
    'admin': {'upw': 'admin123', 'name': '관리자', 'is_admin': True, 'accounts': []}
}
current_user_id = None 

# --- [공통 기능] ---
def add_history(account, detail):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    account['history'].append(f"[{now}] {detail}")

# --- [사용자 인증 기능] ---
def register():
    uid = input("신규 아이디: ")
    if uid in users: return print("이미 존재하는 아이디입니다.")
    upw = input("비밀번호: ")
    name = input("이름: ")
    users[uid] = {'upw': upw, 'name': name, 'is_admin': False, 'accounts': []}
    print(f"'{name}'님, 회원가입을 축하합니다!")

def login():
    global current_user_id
    uid = input("아이디: ")
    upw = input("비밀번호: ")
    if uid in users and users[uid]['upw'] == upw:
        current_user_id = uid
        print(f"로그인 성공! {users[uid]['name']}님 환영합니다.")
    else:
        print("아이디 또는 비밀번호가 틀렸습니다.")

# --- [계좌 관리 기능] ---
def create_account():
    banks = ["하나은행", "우리은행", "국민은행", "신한은행", "기업은행"]
    print(f"지원 은행: {banks}")
    bank = input("은행명: ")
    if bank not in banks: return print("지원하지 않는 은행입니다.")
    
    acc_num = input("계좌번호: ")
    alias = input("계좌 별칭: ")
    try:
        money = int(input("최초 입금액(1000원 이상): "))
        if money < 1000: return print("최초 입금액 미달로 생성이 불가능합니다.")
    except ValueError: return print("숫자만 입력하세요.")

    new_acc = {'bank': bank, 'acc_num': acc_num, 'alias': alias, 'balance': money, 'history': []}
    add_history(new_acc, f"개설 입금: {money}원")
    users[current_user_id]['accounts'].append(new_acc)
    print(f"[{bank}] 계좌가 등록되었습니다.")

def show_my_accounts(target_list=None):
    accs = target_list if target_list is not None else users[current_user_id]['accounts']
    if not accs:
        print("보유한 계좌가 없습니다.")
        return False
    for i, acc in enumerate(accs):
        print(f"{i+1}. [{acc['bank']}] {acc['acc_num']} | 별칭: {acc['alias']} | 잔액: {acc['balance']}원")
    return True

def update_account_alias():
    if not show_my_accounts(): return
    try:
        idx = int(input("수정할 계좌 번호 선택: ")) - 1
        user_accs = users[current_user_id]['accounts']
        new_alias = input("새로운 별칭: ")
        if any(acc['alias'] == new_alias for acc in user_accs):
            return print("오류: 동일한 별칭이 이미 존재합니다.")
        user_accs[idx]['alias'] = new_alias
        print("별칭이 성공적으로 변경되었습니다.")
    except: print("잘못된 입력입니다.")

def delete_account():
    if not show_my_accounts(): return
    try:
        idx = int(input("삭제할 계좌 번호 선택: ")) - 1
        del users[current_user_id]['accounts'][idx]
        print("계좌가 성공적으로 삭제되었습니다.")
    except: print("삭제 실패.")

def search_account():
    keyword = input("\n검색어(별칭/번호/은행): ")
    user_accs = users[current_user_id]['accounts']
    results = [a for a in user_accs if keyword in a['alias'] or keyword in a['acc_num'] or keyword in a['bank']]
    if not results: print("결과가 없습니다.")
    else: show_my_accounts(results)

def transfer():
    if not show_my_accounts(): return
    try:
        idx = int(input("출금할 내 계좌 선택: ")) - 1
        my_acc = users[current_user_id]['accounts'][idx]
        target_uid = input("이체할 상대방 ID: ")
        if target_uid not in users: return print("존재하지 않는 사용자입니다.")
        target_accs = users[target_uid]['accounts']
        if not target_accs: return print("상대방의 계좌가 없습니다.")
        for i, acc in enumerate(target_accs):
            print(f"{i+1}. {acc['bank']} ({acc['acc_num']})")
        t_idx = int(input("상대방 계좌 선택: ")) - 1
        to_acc = target_accs[t_idx]
        amount = int(input("이체 금액: "))
        if amount <= 0: return print("0원 초과 금액만 가능합니다.")
        if my_acc['balance'] < amount: return print("잔액 부족.")
        my_acc['balance'] -= amount
        to_acc['balance'] += amount
        add_history(my_acc, f"이체 출금({to_acc['acc_num']}): {amount}원")
        add_history(to_acc, f"이체 입금({my_acc['acc_num']}): {amount}원")
        print("이체 완료!")
    except: print("오류 발생.")

# --- [관리자 기능] ---
def admin_menu():
    global current_user_id
    print(f"\n=== 관리자 모드 [접속: {users[current_user_id]['name']}] ===")
    print("1. 전체 유저 조회  2. 유저 정보 수정  3. 유저 삭제  4. 로그아웃")
    menu = input("선택: ")
    if menu == '1':
        for uid, info in users.items():
            print(f"ID: {uid} | 이름: {info['name']} | 비번: {info['upw']} | 계좌: {len(info['accounts'])}개")
    elif menu == '2':
        uid = input("수정할 유저 ID: ")
        if uid in users:
            users[uid]['name'] = input("새 이름: ") or users[uid]['name']
            users[uid]['upw'] = input("새 비번: ") or users[uid]['upw']
            print("수정 완료.")
    elif menu == '3':
        uid = input("삭제할 유저 ID: ")
        if uid != 'admin' and uid in users:
            del users[uid]; print("삭제 완료.")
        else: print("삭제 불가.")
    elif menu == '4':
        current_user_id = None

# --- [메인 루프] ---
def main():
    global current_user_id  # 함수 최상단에 위치
    while True:
        if not current_user_id:
            print("\n" + "="*20 + "\n 통합계좌 관리 시스템\n" + "="*20)
            print("1. 회원가입  2. 로그인  3. 종료")
            m = input("선택: ")
            if m == '1': register()
            elif m == '2': login()
            elif m == '3': break
        else:
            if users[current_user_id]['is_admin']:
                admin_menu()
            else:
                print(f"\n--- {users[current_user_id]['name']}님의 은행 메뉴 ---")
                print("1. 계좌 생성  2. 계좌 조회  3. 계좌 수정(별칭)  4. 계좌 삭제")
                print("5. 계좌 검색  6. 계좌 이체  7. 로그아웃")
                m = input("선택: ")
                if m == '1': create_account()
                elif m == '2': show_my_accounts()
                elif m == '3': update_account_alias()
                elif m == '4': delete_account()
                elif m == '5': search_account()
                elif m == '6': transfer()
                elif m == '7': current_user_id = None

if __name__ == "__main__":
    main()
