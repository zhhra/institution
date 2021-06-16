from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField

# ========================================================================================
class Classroom(models.Model):
    room_number= models.IntegerField(unique=True)

    def __str__(self):
        return str(self.room_number)

# ========================================================================================
class Teacher(models.Model):
    first_name= models.CharField(max_length=40)
    last_name= models.CharField(max_length=100)
    birth_year= models.DateField()
    phone_number= PhoneNumberField(blank=True,null=True)
    email=models.EmailField(blank=True,null=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self) -> str:
        return self.full_name()

# ========================================================================================
class Student(models.Model):
    first_name= models.CharField(max_length=40)
    last_name= models.CharField(max_length=100)
    birth_year= models.DateField(blank=True,null=True)
    phone_number= PhoneNumberField(blank=True,null=True)
    email=models.EmailField(blank=True,null=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self) -> str:
        return self.full_name()
# ========================================================================================
class Lesson(models.Model):
    name= models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name

# ========================================================================================
class TheClass(models.Model):
    DAY_CHOICES=[
        ("sa","شنبه"),
        ("su","یکشنبه"),
        ("mo","دوشنبه"),
        ("tu","سه‌شنبه"),
        ("we","چهارشنبه"),
        ("th","پنج‌شنبه"),
        ("fr","جمعه"),

    ]
    classroom= models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL, related_name="Theclasses")
    days= MultiSelectField(choices=DAY_CHOICES)
    start_time= models.TimeField()
    finish_time= models.TimeField()
    lesson=models.ForeignKey(Lesson,  null=True, on_delete=models.SET_NULL, related_name="theclasses")
    teacher= models.ForeignKey(Teacher, null=True, on_delete=models.SET_NULL, related_name="theclasses")
    students= models.ManyToManyField(Student, related_name="theclasses")

    def __str__(self) -> str:
        return f'{self.lesson}-{self.id}'

    def save(self, *args, **kwargs):
        if not self.id:
            classroom= self.classroom
            days= self.days
            start_time= self.start_time
            finish_time= self.finish_time
            lesson=self.lesson
            teacher= self.teacher
            for theclass in TheClass.objects.filter(classroom=classroom):
                for day in days:
                    if day in theclass.days:
                        if start_time > finish_time:
                            raise Exception("زمان شروع یا پایان ایراد دارد")
                        if start_time >= theclass.start_time and theclass.finish_time >= start_time:
                            raise Exception("زمان ها تداخل دارند")
            
            
            for theclass in teacher.theclasses.all():
                for day in days:
                    if day in theclass.days:
                        if start_time >= theclass.start_time and theclass.finish_time >= start_time:
                            raise Exception("تداخل در برنامه معلم")

            for theclass in TheClass.objects.all():
                for student in theclass.students.all():
                    for item in student.theclasses.all():
                        for day in days:
                            if day in item.days:
                                if start_time >= item.start_time and item.finish_time >= start_time:
                                    raise Exception("تداخل در برنامه دانشجو") 

            super(TheClass, self).save(*args, **kwargs)

