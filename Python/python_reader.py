import requests
import json
import time
from datetime import datetime

# Firebase configuration
DATABASE_URL = "(database URL kamu)"

def get_data_from_path(path):
    """Get data from a specific Firebase path using REST API"""
    try:
        url = f"{DATABASE_URL}/{path}.json"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching {path}: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching {path}: {e}")
        return None

def get_data_once():
    """Get data from Firebase once"""
    try:
        print(f"Fetching data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Get data from each path
        counter = get_data_from_path("Data/counter")
        jam = get_data_from_path("Waktu/Jam")
        menit = get_data_from_path("Waktu/Menit")
        
        print(f"Counter: {counter}")
        print(f"Jam: {jam}")
        print(f"Menit: {menit}")
        
        if jam is not None and menit is not None:
            print(f"Time: {jam:02d}:{menit:02d}")
        else:
            print("Time: N/A")
        
        print("-" * 40)
        
        return {
            'counter': counter,
            'jam': jam,
            'menit': menit
        }
        
    except Exception as e:
        print(f"Error reading data: {e}")
        return None

def monitor_data_continuously():
    """Monitor data changes continuously"""
    print("Starting continuous monitoring...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            data = get_data_once()
            if data:
                # You can add your data processing logic here
                pass
            time.sleep(5)  # Wait 5 seconds before next read
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")

def get_all_data():
    """Get all data from the database"""
    try:
        print("Fetching all database data...")
        url = f"{DATABASE_URL}/.json"
        response = requests.get(url)
        
        if response.status_code == 200:
            all_data = response.json()
            print("All database data:")
            print(json.dumps(all_data, indent=2))
            return all_data
        else:
            print(f"Error fetching all data: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error getting all data: {e}")
        return None

def test_connection():
    """Test connection to Firebase"""
    try:
        print("Testing connection to Firebase...")
        url = f"{DATABASE_URL}/.json"
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✓ Connection successful!")
            return True
        else:
            print(f"✗ Connection failed: HTTP {response.status_code}")
            if response.status_code == 401:
                print("This indicates authentication/permission issues.")
                print("Make sure your Firebase database rules allow public read access.")
            return False
            
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

def show_database_rules_help():
    """Show help for setting up database rules"""
    print("\n" + "="*50)
    print("FIREBASE DATABASE RULES SETUP")
    print("="*50)
    print("To allow public read access, set your Firebase database rules to:")
    print()
    print('{')
    print('  "rules": {')
    print('    ".read": true,')
    print('    ".write": "auth != null"')
    print('  }')
    print('}')
    print()
    print("Steps:")
    print("1. Go to Firebase Console")
    print("2. Select your project")
    print("3. Go to Realtime Database")
    print("4. Click on 'Rules' tab")
    print("5. Replace existing rules with the above")
    print("6. Click 'Publish'")
    print("="*50)

def main():
    """Main function"""
    print("Firebase RTDB Data Reader (REST API)")
    print("=" * 50)
    
    # Test connection first
    if not test_connection():
        show_database_rules_help()
        return
    
    while True:
        print("\nOptions:")
        print("1. Get data once")
        print("2. Monitor data continuously")
        print("3. Get all database data")
        print("4. Test connection")
        print("5. Show database rules help")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            get_data_once()
        elif choice == '2':
            monitor_data_continuously()
        elif choice == '3':
            get_all_data()
        elif choice == '4':
            test_connection()
        elif choice == '5':
            show_database_rules_help()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
