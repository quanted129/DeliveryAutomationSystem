# will call services.routing_engine module at pre-defined triggers
# planned triggers:
# 0. immediately upon startup if no orders assigned!!!
# 1. once every minute (check urgency)
# 2. when order added with endTime < datetime.now() + buffer
# 3. when end time of potential route is near endTime of last order in potential route