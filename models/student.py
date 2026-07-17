class Student:
   """Represents a student with basic academic and contact information."""
   def __init__(self,
                id:int, 
                name:str,
                age:int,
                department:str,
                email:str,
                cgpa:float):
      
      self.id = id 
      self.name = name
      self.age = age
      self.department = department
      self.email = email 
      self.cgpa = cgpa

   def __str__(self):
      """this give an understandable return value"""
      return f"stundent {self.id}: {self.name} ({self.department} - cgpa is {self.cgpa})"
   
   def to_tuple(self):
      """Converts the student's attributes into a standard tuple layout"""
      return(self.id, 
            self.name,
            self.age,
            self.department,
            self.email, 
            self.cgpa)