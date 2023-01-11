from haversine import haversine, Unit

if __name__ == "__main__":
    # 两点的经纬度
    point1 = (30.519695, 120.948112)
    point2 = (30.537681519116482, 120.948112)
    result1 = haversine(point1, point2, unit=Unit.KILOMETERS)  # km
    result2 = haversine(point1, point2, unit=Unit.METERS)  # m
    # 打印计算结果
    print("距离：{:.3f}km".format(result1))
    print("距离：{:.3f}m".format(result2))




# if __name__ == "__main__":
#     result = get_distance_hav(30.519695, 120.948112, 30.56145070412892, 120.948112)
#     print("距离：{:.3}km".format(result))
(120.948112, 30.537681519116482)