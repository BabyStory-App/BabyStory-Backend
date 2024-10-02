# from datetime import datetime, timedelta
# import random

# from db import get_db_session

# db = get_db_session()
# check_query = "SELECT COUNT(*) FROM babystate WHERE baby_id = 'b-5116'"
# result = db.execute(check_query).scalar()

# if result == 0:
#     # P001 부모의 아기들 ID 가져오기
#     baby_ids_query = "SELECT baby_id FROM pbconnect WHERE parent_id = 'P001'"
#     baby_ids = [row[0] for row in db.execute(baby_ids_query)]

#     # 각 아기에 대해 100개의 상태 데이터 생성
#     for idx, baby_id in enumerate(baby_ids):
#         insert_query = """
#         INSERT INTO babystate (baby_id, createTime, cm, kg)
#         VALUES (:baby_id, :createTime, :cm, :kg)
#         """

#         # 각 아기마다 다른 시작 시간 설정
#         start_time = datetime.now() - timedelta(days=2, hours=idx)

#         data = [
#             {
#                 'baby_id': baby_id,
#                 'createTime': start_time + timedelta(minutes=i*15),  # 15분씩 증가
#                 'cm': round(random.uniform(40, 60), 2),
#                 'kg': round(random.uniform(2, 10), 2)
#             }
#             for i in range(100)
#         ]

#         db.execute(insert_query, data)

#     db.commit()
