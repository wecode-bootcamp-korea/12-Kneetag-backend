def message(domain, token, name):
    return f"아래 링크를 클릭하면 회원가입이 완료됩니다. \n\n아래 링크를 클릭한 후 비밀번호를 새로 생성하여 이용해 주세요.\n\n name:{name}\n\n \
    회원가입인증 링크 : http://{domain}/mypage?key={token}\n\n감사합니다."