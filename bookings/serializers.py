from django.utils import timezone
from rest_framework import serializers
from .models import Booking

class CreateRoomBookingSerializer(serializers.ModelSerializer):
        
        check_in = serializers.DateField() # models에선 null=True, blank=True로 설정했지만 여기선 필수로 설정
        check_out = serializers.DateField()
        
        class Meta:
            model = Booking
            fields = ( # user에게 받고 싶은 data를 정의
                "check_in",
                "check_out",
                "guests",
            )
        def validate_check_in(self, value): # 특정 필드의 validation을 커스텀하는 방법, value는 사용자가 입력한 값
            now = timezone.localtime(timezone.now()).date() # 현재 날짜
            check_out = self.initial_data.get("check_out") # 사용자가 입력한 check_out 값
            if now > value:
                raise serializers.ValidationError("Check-in date must be future.")
            if value >= check_out:
                raise serializers.ValidationError("Check-out date must be later than check-in date.")
            return value # return value를 하면 성공적으로 validation을 통과한 것으로 간주
        
        def validate_check_out(self, value): # 특정 필드의 validation을 커스텀하는 방법, value는 사용자가 입력한 값
            now = timezone.localtime(timezone.now()).date() # 현재 날짜
            check_in = self.initial_data.get("check_in") # 사용자가 입력한 check_in 값
            if now > value:
                raise serializers.ValidationError("Check-in date must be future.")
            if value <= check_in:
                raise serializers.ValidationError("Check-out date must be later than check-in date.")
            return value # return value를 하면 성공적으로 validation을 통과한 것으로 간주
        
        
        

class PublicBookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests", 
        )