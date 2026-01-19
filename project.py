import json
import os
from datetime import datetime
from collections import Counter

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️  Error loading tasks. Starting fresh.")
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)
        print("✅ Tasks saved successfully!")
    
    def add_task(self):
        """Add a new task"""
        print("\n" + "="*50)
        print("📝 CREATE NEW TASK")
        print("="*50)
        
        title = input("Title: ").strip()
        if not title:
            print("❌ Title cannot be empty!")
            return
        
        description = input("Description: ").strip()
        
        print("\nPriority (low/medium/high): ", end="")
        priority = input().strip().lower()
        if priority not in ['low', 'medium', 'high']:
            priority = 'medium'
        
        print("Status (todo/in-progress/completed): ", end="")
        status = input().strip().lower()
        if status not in ['todo', 'in-progress', 'completed']:
            status = 'todo'
        
        print("Category (Development/Design/Testing/Documentation/Security/Database): ", end="")
        category = input().strip()
        if not category:
            category = 'General'
        
        print("Due Date (YYYY-MM-DD) [optional]: ", end="")
        due_date = input().strip()
        
        print("Estimated Hours: ", end="")
        try:
            estimated_hours = int(input().strip() or 0)
        except ValueError:
            estimated_hours = 0
        
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'priority': priority,
            'status': status,
            'category': category,
            'due_date': due_date,
            'created_at': datetime.now().strftime('%Y-%m-%d'),
            'estimated_hours': estimated_hours,
            'actual_hours': 0
        }
        
        self.tasks.append(task)
        self.save_tasks()
        print(f"\n✅ Task '{title}' created successfully!")
    
    def view_tasks(self, filter_status=None):
        """Display all tasks or filtered tasks"""
        if not self.tasks:
            print("\n📭 No tasks found. Create one to get started!")
            return
        
        tasks_to_show = self.tasks
        if filter_status:
            tasks_to_show = [t for t in self.tasks if t['status'] == filter_status]
        
        if not tasks_to_show:
            print(f"\n📭 No tasks found with status: {filter_status}")
            return
        
        print("\n" + "="*80)
        print("📋 TASK LIST")
        print("="*80)
        
        for task in tasks_to_show:
            self.display_task(task)
    
    def display_task(self, task):
        """Display a single task with formatting"""
        priority_symbols = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}
        status_symbols = {
            'todo': '⏳',
            'in-progress': '🔄',
            'completed': '✅',
            'overdue': '⚠️'
        }
        
        print(f"\n{status_symbols.get(task['status'], '📌')} ID: {task['id']} | {priority_symbols.get(task['priority'], '')} {task['title']}")
        print(f"   Description: {task['description']}")
        print(f"   Category: {task['category']} | Priority: {task['priority'].upper()} | Status: {task['status'].upper()}")
        
        if task['due_date']:
            print(f"   Due Date: {task['due_date']}", end="")
            # Check if overdue
            try:
                due = datetime.strptime(task['due_date'], '%Y-%m-%d')
                if due < datetime.now() and task['status'] != 'completed':
                    print(" ⚠️ OVERDUE!", end="")
            except:
                pass
            print()
        
        print(f"   Hours: Estimated {task['estimated_hours']}h | Actual {task['actual_hours']}h")
        
        if task['actual_hours'] > 0 and task['estimated_hours'] > 0:
            if task['actual_hours'] <= task['estimated_hours']:
                print(f"   ✅ On track!")
            else:
                print(f"   ⚠️  Over estimate by {task['actual_hours'] - task['estimated_hours']}h")
        
        print("-" * 80)
    
    def edit_task(self):
        """Edit an existing task"""
        self.view_tasks()
        
        try:
            task_id = int(input("\nEnter Task ID to edit: "))
            task = next((t for t in self.tasks if t['id'] == task_id), None)
            
            if not task:
                print("❌ Task not found!")
                return
            
            print(f"\n📝 Editing: {task['title']}")
            print("(Press Enter to keep current value)\n")
            
            title = input(f"Title [{task['title']}]: ").strip()
            if title:
                task['title'] = title
            
            description = input(f"Description [{task['description']}]: ").strip()
            if description:
                task['description'] = description
            
            priority = input(f"Priority [{task['priority']}]: ").strip().lower()
            if priority in ['low', 'medium', 'high']:
                task['priority'] = priority
            
            status = input(f"Status [{task['status']}]: ").strip().lower()
            if status in ['todo', 'in-progress', 'completed']:
                task['status'] = status
            
            actual_hours = input(f"Actual Hours [{task['actual_hours']}]: ").strip()
            if actual_hours:
                try:
                    task['actual_hours'] = int(actual_hours)
                except ValueError:
                    pass
            
            self.save_tasks()
            print("\n✅ Task updated successfully!")
            
        except ValueError:
            print("❌ Invalid input!")
    
    def delete_task(self):
        """Delete a task"""
        self.view_tasks()
        
        try:
            task_id = int(input("\nEnter Task ID to delete: "))
            task = next((t for t in self.tasks if t['id'] == task_id), None)
            
            if not task:
                print("❌ Task not found!")
                return
            
            confirm = input(f"Are you sure you want to delete '{task['title']}'? (yes/no): ").lower()
            if confirm == 'yes':
                self.tasks.remove(task)
                self.save_tasks()
                print("✅ Task deleted successfully!")
            else:
                print("❌ Deletion cancelled.")
                
        except ValueError:
            print("❌ Invalid input!")
    
    def show_analytics(self):
        """Display task analytics"""
        if not self.tasks:
            print("\n📭 No tasks to analyze!")
            return
        
        print("\n" + "="*60)
        print("📊 TASK ANALYTICS")
        print("="*60)
        
        # Status counts
        statuses = [t['status'] for t in self.tasks]
        status_counts = Counter(statuses)
        
        print("\n📈 Status Distribution:")
        for status, count in status_counts.items():
            percentage = (count / len(self.tasks)) * 100
            bar = "█" * int(percentage / 5)
            print(f"  {status.upper():15} | {bar} {count} ({percentage:.1f}%)")
        
        # Priority counts
        priorities = [t['priority'] for t in self.tasks]
        priority_counts = Counter(priorities)
        
        print("\n🎯 Priority Distribution:")
        for priority, count in priority_counts.items():
            symbols = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}
            print(f"  {symbols.get(priority, '')} {priority.upper():10} | {count} tasks")
        
        # Category counts
        categories = [t['category'] for t in self.tasks]
        category_counts = Counter(categories)
        
        print("\n📁 Category Distribution:")
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category:20} | {count} tasks")
        
        # Time tracking
        total_estimated = sum(t['estimated_hours'] for t in self.tasks)
        total_actual = sum(t['actual_hours'] for t in self.tasks)
        
        print("\n⏱️  Time Tracking:")
        print(f"  Total Estimated: {total_estimated}h")
        print(f"  Total Actual:    {total_actual}h")
        
        if total_estimated > 0:
            efficiency = (total_estimated / total_actual * 100) if total_actual > 0 else 0
            print(f"  Efficiency:      {efficiency:.1f}%")
            
            if efficiency > 100:
                print("  ✅ Under estimated time!")
            elif efficiency < 100:
                print("  ⚠️  Over estimated time")
        
        # Completion rate
        completed = status_counts.get('completed', 0)
        completion_rate = (completed / len(self.tasks)) * 100
        print(f"\n🎯 Completion Rate: {completion_rate:.1f}% ({completed}/{len(self.tasks)})")
        
        print("="*60)
    
    def search_tasks(self):
        """Search tasks by keyword"""
        keyword = input("\n🔍 Enter search keyword: ").strip().lower()
        
        if not keyword:
            print("❌ Please enter a search term!")
            return
        
        results = [
            t for t in self.tasks 
            if keyword in t['title'].lower() 
            or keyword in t['description'].lower()
            or keyword in t['category'].lower()
        ]
        
        if not results:
            print(f"\n📭 No tasks found matching '{keyword}'")
            return
        
        print(f"\n🔍 Found {len(results)} task(s) matching '{keyword}':")
        for task in results:
            self.display_task(task)


def main():
    """Main program loop"""
    manager = TaskManager()
    
    while True:
        print("\n" + "="*60)
        print("🎯 TASK MANAGEMENT SYSTEM")
        print("="*60)
        print("1. ➕ Add New Task")
        print("2. 📋 View All Tasks")
        print("3. 🔍 Search Tasks")
        print("4. ✏️  Edit Task")
        print("5. 🗑️  Delete Task")
        print("6. 📊 View Analytics")
        print("7. 🔧 Filter by Status")
        print("8. 💾 Save & Exit")
        print("="*60)
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            manager.add_task()
        elif choice == '2':
            manager.view_tasks()
        elif choice == '3':
            manager.search_tasks()
        elif choice == '4':
            manager.edit_task()
        elif choice == '5':
            manager.delete_task()
        elif choice == '6':
            manager.show_analytics()
        elif choice == '7':
            print("\nFilter by status:")
            print("1. Todo")
            print("2. In Progress")
            print("3. Completed")
            
            filter_choice = input("Choose (1-3): ").strip()
            status_map = {'1': 'todo', '2': 'in-progress', '3': 'completed'}
            
            if filter_choice in status_map:
                manager.view_tasks(status_map[filter_choice])
        elif choice == '8':
            manager.save_tasks()
            print("\n👋 Goodbye! Your tasks are saved.")
            break
        else:
            print("❌ Invalid choice! Please enter 1-8.")


if __name__ == "__main__":
    print("="*60)
    print("🚀 Welcome to Task Management System!")
    print("="*60)
    main()