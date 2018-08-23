import random


class YunPian:
    """调用云片网发送短信验证码"""

    def generate_code(self):
        """生成六位验证码"""
        seeds = '0123456789'
        random_lst = []
        for i in range(6):
            random_lst.append(random.choice(seeds))
        return ''.join(random_lst)

    def send(self, mobile):
        sms_code = self.generate_code()
        print(sms_code)
        return {'status': 0, 'mobile': mobile, 'sms_code': sms_code}
