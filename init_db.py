from gate import app, db, Student
import os

with app.app_context():
    # Create all tables
    db.create_all()

    # Check if we already have data
    existing_count = Student.query.count()
    if existing_count > 0:
        print(f"Database already has {existing_count} students. Skipping population.")
    else:
        # Add sample students
        students_data = [
            {"student_number": "12345", "name": "Alice Johnson", "fee_cleared": True},
            {"student_number": "12346", "name": "Bob Smith", "fee_cleared": False},
            {"student_number": "12347", "name": "Charlie Brown", "fee_cleared": True},
            {"student_number": "12348", "name": "Diana Prince", "fee_cleared": False},
            {"student_number": "12349", "name": "John Smith", "fee_cleared": True},
            {"student_number": "12350", "name": "Jane Doe", "fee_cleared": False},
            {"student_number": "12351", "name": "Bob Johnson", "fee_cleared": True},
            {"student_number": "12352", "name": "Alice Brown", "fee_cleared": True},
            {"student_number": "12353", "name": "Mary Johnson", "fee_cleared": True},
            {"student_number": "12354", "name": "David Wilson", "fee_cleared": False},
            {"student_number": "12355", "name": "Sarah Davis", "fee_cleared": True},
            {"student_number": "12356", "name": "Michael Brown", "fee_cleared": False},
        ]

        added_count = 0
        for data in students_data:
            try:
                student = Student(
                    student_number=data["student_number"],
                    name=data["name"],
                    fee_cleared=data["fee_cleared"]
                )
                db.session.add(student)
                added_count += 1
            except Exception as e:
                print(f"Error adding {data['name']}: {e}")

        try:
            db.session.commit()
            print(f"✅ Successfully added {added_count} students to the database!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error committing to database: {e}")

    # Show current database status
    total_students = Student.query.count()
    cleared_count = Student.query.filter_by(fee_cleared=True).count()
    print(f"📊 Database Status: {total_students} total students, {cleared_count} with cleared fees")