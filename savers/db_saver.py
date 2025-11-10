import boto3
import os
from typing import Any, Dict
from datetime import datetime
from dotenv import load_dotenv
from .base_saver import BaseSaver
from utils.logger import Logging

# 환경변수 로드
load_dotenv()

class DynamoDBSaver(BaseSaver):
    """AWS DynamoDB에 저장하는 구현체."""

    def __init__(
        self,
        table_name: str = None,
        region_name: str = None
    ):
        """
        DynamoDB 클라이언트 초기화.
        환경변수에서 설정을 자동으로 읽어옵니다.
        
        Args:
            table_name: DynamoDB 테이블 이름 (기본값: 환경변수 DYNAMODB_TABLE_NAME)
            region_name: AWS 리전 (기본값: 환경변수 AWS_REGION 또는 ap-northeast-2)
        """
        # 환경변수에서 설정 읽기
        self.table_name = table_name or os.getenv("DYNAMODB_TABLE_NAME", "stock_news")
        region = region_name or os.getenv("AWS_REGION", "ap-northeast-2")
        
        # DynamoDB 클라이언트 생성 (환경변수나 IAM Role에서 자동 인증)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.table = self.dynamodb.Table(self.table_name)

    def save(self, data: Dict[str, Any], path: str = None) -> str:
        """
        데이터를 DynamoDB에 저장하고 저장된 항목의 ID를 반환한다.
        
        Args:
            data: 저장할 데이터 (Dict 형태)
            path: DynamoDB에서는 사용하지 않지만, 인터페이스 통일을 위해 유지
                  (대신 'id' 키로 파티션 키를 지정할 수 있음)
        
        Returns:
            저장된 항목의 ID (파티션 키 값)
        """
        # 타임스탬프 추가
        if 'created_at' not in data:
            data['created_at'] = datetime.now().isoformat()
        
        # ID가 없으면 자동 생성 (타임스탬프 기반)
        if 'id' not in data:
            data['id'] = f"{datetime.now().timestamp()}"
        
        # DynamoDB에 저장
        self.table.put_item(Item=data)
        
        return data['id']
    
    def get(self, item_id: str) -> Dict[str, Any]:
        """
        DynamoDB에서 데이터를 조회한다.
        
        Args:
            item_id: 조회할 항목의 ID (파티션 키)
        
        Returns:
            조회된 데이터
        """
        response = self.table.get_item(Key={'id': item_id})
        return response.get('Item', {})
    
    def update(self, item_id: str, data: Dict[str, Any]) -> str:
        """
        DynamoDB의 기존 항목을 업데이트한다.
        
        Args:
            item_id: 업데이트할 항목의 ID
            data: 업데이트할 데이터
        
        Returns:
            업데이트된 항목의 ID
        """
        data['updated_at'] = datetime.now().isoformat()
        data['id'] = item_id
        
        self.table.put_item(Item=data)
        return item_id
    
    def delete(self, item_id: str) -> bool:
        """
        DynamoDB에서 항목을 삭제한다.
        
        Args:
            item_id: 삭제할 항목의 ID
        
        Returns:
            삭제 성공 여부
        """
        try:
            self.table.delete_item(Key={'id': item_id})
            return True
        except Exception as e:
            Logging.error(f"삭제 실패: {e}")
            return False