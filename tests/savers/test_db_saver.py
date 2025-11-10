"""DynamoDBSaver 테스트 스크립트"""

from savers.db_saver import DynamoDBSaver
from utils.logger import Logging
from datetime import datetime

def test_dynamodb_saver():
    """DynamoDB 저장 기능 테스트"""

    # 테스트 데이터
    test_data = {
        "company": "삼성전자",
        "news": [
            {
                "title": "테스트 뉴스 1",
                "link": "https://example.com/1",
                "pub_date": datetime.now().isoformat(),
                "source": "테스트 소스"
            }
        ]
    }

    # DynamoDB Saver 초기화
    Logging.info("DynamoDB Saver 초기화 중...")
    saver = DynamoDBSaver()

    # 저장 테스트
    Logging.info("데이터 저장 중...")
    item_id = saver.save(test_data)
    Logging.success(f"저장 완료! ID: {item_id}")

    # 조회 테스트
    Logging.info(f"저장된 데이터 조회 중... (ID: {item_id})")
    retrieved_data = saver.get(item_id)
    Logging.success(f"조회 완료! 데이터: {retrieved_data}")

    # 업데이트 테스트
    Logging.info(f"데이터 업데이트 중... (ID: {item_id})")
    test_data["company"] = "SK하이닉스"
    saver.update(item_id, test_data)
    Logging.success("업데이트 완료!")

    # 업데이트 확인
    updated_data = saver.get(item_id)
    Logging.info(f"업데이트된 데이터: {updated_data}")

    # 삭제 테스트 (선택사항 - 주석 처리)
    # Logging.info(f"데이터 삭제 중... (ID: {item_id})")
    # result = saver.delete(item_id)
    # Logging.success(f"삭제 {'성공' if result else '실패'}!")

if __name__ == "__main__":
    try:
        test_dynamodb_saver()
        Logging.success("모든 테스트 완료!")
    except Exception as e:
        Logging.error(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
