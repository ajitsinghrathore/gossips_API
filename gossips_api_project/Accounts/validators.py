from django.core.validators import RegexValidator


username_validator =  RegexValidator(
                        regex = "^[0-9a-zA-Z_]{1,}$",
                        message= "username must be alphanumeric and length  should be grater than 5"     
                            )

real_name_validator = RegexValidator(
                        regex = "^[a-zA-Z ]+$",
                        message =  "your name should  contain only alpahabets"
                       )    


password_validator = RegexValidator(regex = "^[0-9a-zA-Z_]{8,}$" , message = "password must be alphanumeric and length should be greater than 8")

phone_validator = RegexValidator(regex = "^(91)[0-9]{10}$" , message = "not eligible phone number")                                               