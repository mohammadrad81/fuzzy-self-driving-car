from typing import Tuple
class FuzzyGasController:
    """
    # emtiazi todo
    write all the fuzzify,inference,defuzzify method in this class
    """

    def __init__(self, union_function=max, intersection_function=min):
        self.union_function = union_function
        self.intersection_function = intersection_function


    def __fuzzify_center_distance(self, center_distance: float)->Tuple[float, float, float]:
        close = 0.0
        moderate = 0.0
        far = 0.0
        if 0 <= center_distance <= 40:
            close = 1/50 * center_distance + 1

        elif 40 <= center_distance <= 50:
            moderate = 1/10 * center_distance - 4
            close = 1/50 * center_distance + 1

        elif 50 <= center_distance <= 90:
            moderate = (-1/50) * center_distance + 2

        elif 90 <= center_distance <= 200:
            moderate = (-1/50) * center_distance + 2
            far = 1/110 * center_distance - 90/110

        elif center_distance > 200:
            far = 1

        return close, moderate, far

    def __get_low_speed_membership_by_rules(self, close: float)->float:
        return close

    def __get_medium_membership_by_rules(self, moderate: float)->float:
        return moderate

    def __get_high_membership_by_rules(self, far)->float:
        return far

    def __max_membership(self,
                         speed: float,
                         close: float,
                         moderate: float,
                         far: float)->float:
        low = 0.0
        medium = 0.0
        high = 0.0

        if 0.0 <= speed <= 5:
            low = 1/5 * speed
            medium = 1/15 * speed

        elif 5.0 <= speed <= 10.0:
            low = (-1/5) * speed + 2
            medium = 1/15 * speed

        elif 10 <= speed <= 15:
            medium = 1/15 * speed

        elif 15 <= speed <= 25:
            medium = (-1/15) * speed + 2

        elif 25 <= speed <= 30:
            medium = (-1/15) * speed + 2
            high = 1/5 * speed - 5

        elif 30 <= speed <= 90:
            high = (-1/60) * speed + 3/2

        low = min(low, self.__get_low_speed_membership_by_rules(close))
        medium = min(medium, self.__get_medium_membership_by_rules(moderate))
        high = min(high, self.__get_high_membership_by_rules(far))
        # print(f"low: {low}, medium: {medium}, high: {high}")
        return max(low, medium, high)

    def __float_range(self, start: float=0.0, end: float=1, count_of_steps: float=1000):
        s = start
        step = (end - start) / count_of_steps
        while s < end:
            yield s
            s += step


    def __defuzzify(self,
                    close: float,
                    moderate: float,
                    far: float)->float:
        dividant = 0.0
        divider = 0.0
        COUNT_OF_STEPS = 10000
        delta = 90/COUNT_OF_STEPS
        speed_magnitudes = self.__float_range(0, 90, COUNT_OF_STEPS)
        for speed in speed_magnitudes:
            max_membership = self.__max_membership(speed,
                                                   close,
                                                   moderate,
                                                   far)
            dividant += max_membership * speed * delta
            divider += max_membership * delta
        center = 0
        if divider != 0:
            center = 1.0 * float(dividant) / float(divider)
        return center


    def decide(self, center_dist):
        """
        main method for doin all the phases and returning the final answer for gas
        """
        close, moderate, far = self.__fuzzify_center_distance(center_dist)
        decision = self.__defuzzify(close, moderate, far)
        return decision
    