from curvepost.curve_util import cal_speed


class CurveCalculator:
    cal_speed = staticmethod(cal_speed)

    @staticmethod
    def cal_cant(speed: float, radius: float, original_cant: float) -> float:
        if original_cant == 0:
            value = 11.8 * (speed ** 2) / radius
            return min(value, 160)
        return original_cant

    @staticmethod
    def cal_slack(radius: float) -> float:
        slack = 2400 / radius
        return slack - 5 if slack >= 30 else slack
