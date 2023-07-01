from typing import Dict, Set, List, Tuple


class FuzzyController:
    """
    #todo
    write all the fuzzify,inference,defuzzify method in this class
    """

    def __init__(self, union_function=max, intersection_function=min):
        self.union_function = union_function
        self.intersection_function = intersection_function

    def __fuzzify_distance(self, distance: float) -> Tuple[float, float, float]:
        """
        fuzzifies the distance
        Args:
            distance: the distance

        Returns: the fuzzified output of distance, close, moderate, far
        """
        close = max(0, (1 - ((1 / 50) * distance)))
        close = min(1, close)
        far = max(0, (-1 + ((1 / 50) * distance)))
        far = min(1, far)
        moderate = 0
        if 35 < distance < 65:
            if distance < 50:
                tmp = distance - 35
                moderate = 1 / 15 * tmp
            else:
                tmp = distance - 50
                moderate = 1 - 1 / 15 * tmp
        return close, moderate, far

    def __float_range(self, start: float=0.0, end: float=1, count_of_steps: float=1000):
        s = start
        step = (end - start) / count_of_steps
        while s < end:
            yield s
            s += step

    def __get_low_right_membership_by_rules(self, close_left: float, moderate_right: float) -> float:
        return self.intersection_function(close_left, moderate_right)

    def __get_high_right_membership_by_rules(self, close_left: float, far_right: float) -> float:
        return self.intersection_function(close_left, far_right)

    def __get_low_left_membership_by_rules(self, moderate_left: float, close_right: float) -> float:
        return self.intersection_function(moderate_left, close_right)

    def __get_high_left_membership_by_rules(self, far_left: float, close_right: float) -> float:
        return self.intersection_function(far_left, close_right)

    def __get_nothing_membership_by_rules(self, moderate_left: float, moderate_right: float) -> float:
        return self.intersection_function(moderate_left, moderate_right)

    def __max_membership(self,
                         rotation: float,
                         close_left: float,
                         moderate_left: float,
                         far_left: float,
                         close_right: float,
                         moderate_right: float,
                         far_right: float):
        high_right = 0.0
        low_right = 0.0
        nothing = 0.0
        low_left = 0.0
        high_left = 0.0

        if -50 <= rotation <= -20:
            high_right = (1/30) * rotation + 5/3
        elif -20 <= rotation <= -10:
            high_right = (-1/15) * rotation - 1/3
            low_right = 1/10 * rotation + 2

        elif -10 <= rotation <= -5:
            high_right = (-1/15) * rotation - 1/3
            low_right = (-1/10) * rotation
            nothing = (1/10) * rotation + 1

        elif -5 <= rotation <= 0:
            low_right = (-1/10) * rotation
            nothing = (1/10) * rotation + 1

        elif 0 <= rotation <= 5:
            nothing = (-1/10) * rotation + 1
            low_left = (1/10) * rotation

        elif 5 <= rotation <= 10:
            nothing = (-1/10) * rotation + 1
            low_left = (1/10) * rotation
            high_left = (1/15) * rotation - 1/3

        elif 10 <= rotation <= 20:
            low_left = (-1/10) * rotation + 2
            high_left = (1/15) * rotation - 1/3

        elif 20 <= rotation <= 50:
            high_left = (-1/30) * rotation + 5/3
        high_right = min(high_right, self.__get_high_right_membership_by_rules(close_left, far_right))
        low_right = min(low_right, self.__get_low_right_membership_by_rules(close_left, moderate_right))
        nothing = min(nothing, self.__get_nothing_membership_by_rules(moderate_left, moderate_right))
        low_left = min(low_left, self.__get_low_left_membership_by_rules(moderate_left, close_right))
        high_left = min(high_left, self.__get_high_left_membership_by_rules(far_left, close_right))

        decision = max(high_right, low_right, nothing, low_left, high_left)
        return decision

    def __defuzzification(self,
                          far_left: float,
                          moderate_left: float,
                          close_left: float,
                          close_right: float,
                          moderate_right: float,
                          far_right: float):
        dividant = 0.0
        divider = 0.0
        COUNT_OF_STEPS = 10000
        rotation_magnitudes = self.__float_range(-50, 50, COUNT_OF_STEPS)
        delta = 100 / COUNT_OF_STEPS
        for rotation in rotation_magnitudes:
            max_membership = self.__max_membership(rotation,
                                                   close_left,
                                                   moderate_left,
                                                   far_left,
                                                   close_right,
                                                   moderate_right,
                                                   far_right)
            dividant += max_membership * rotation * delta
            divider += max_membership * delta
        center = 0
        if divider != 0:
            center = 1.0 * float(dividant)/float(divider)
        return center


    def decide(self, left_dist, right_dist):
        """
        main method for doin all the phases and returning the final answer for rotation
        """
        close_left, moderate_left, far_left = self.__fuzzify_distance(left_dist)
        close_right, moderate_right, far_right = self.__fuzzify_distance(right_dist)
        decision = self.__defuzzification(far_left,
                                          moderate_left,
                                          close_left,
                                          close_right,
                                          moderate_right,
                                          far_right)

        return decision
