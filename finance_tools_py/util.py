import random


class Random():
    @staticmethod
    def random_with_topic(topic="SYMBOL", lens=8):
        """生成随机值。

        SYMBOL+4数字id+4位大小写随机

        Args:
            lens: 数字字符长度

        Returns:

        """
        _list = [chr(i) for i in range(65,
                                       91)] + [chr(i) for i in range(97,
                                                                     123)
                                               ] + [str(i) for i in range(10)]
        num = random.sample(_list, lens)
        return '{}_{}'.format(topic, ''.join(num))
