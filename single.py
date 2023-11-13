
class Solver:
    def __init__(self, capacity, time_limit, num_scooters, priorities, distances):
        self.capacity = capacity
        self.time_limit = time_limit
        self.num_scooters = num_scooters
        self.priorities = priorities
        self.distances = distances
    
    def optimal_itenerary(self):
        #WARNING: O(N!) complexity
        pass
    
    def solve(self):
        # Создаем список самокатов с информацией о приоритетах и расстояниях
        scooters = []
        for i in range(self.num_scooters):
            scooter = {
                'priority': self.priorities[i],
                'distance': self.distances[i + 1][0]  # Расстояние от начальной точки к самокату
            }
            scooters.append(scooter)
        
        # Сортируем список самокатов по приоритетам в убывающем порядке
        scooters.sort(key=lambda x: x['priority'], reverse=True)
        
        # Объявляем переменные для отслеживания текущего времени и количества замененных аккумуляторов
        current_time = 0
        replaced_count = 0
        
        # Список самокатов, которые будут заменены
        to_be_replaced = []
        
        for scooter in scooters:
            # Проверяем, поместится ли самокат в рюкзаке курьера и не будет ли превышено время limit
            if current_time + scooter['distance'] <= self.time_limit and replaced_count + scooter['priority'] <= self.capacity:
                to_be_replaced.append(scooter)
                current_time += scooter['distance']
                replaced_count += scooter['priority']
        
        # Выводим результаты
        print("Маршрут:")
        print("Начальная точка ->", end=' ')
        for scooter in to_be_replaced:
            print("Самокат", scooters.index(scooter) + 1, "->", end=' ')
        print("Конечная точка")
        print("Сумма приоритетов:", replaced_count)
