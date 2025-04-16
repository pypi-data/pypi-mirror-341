from securepassgen_advanced.generator import generate_password  # Import from the generator module


def main():
    print("\n🔐 SecurePassGen CLI 🔐")

    try:
        length = int(input("Enter password length: "))
        use_upper = input("Include uppercase? (y/n): ").strip().lower() == 'y'
        use_lower = input("Include lowercase? (y/n): ").strip().lower() == 'y'
        use_digits = input("Include digits? (y/n): ").strip().lower() == 'y'
        use_symbols = input("Include symbols? (y/n): ").strip().lower() == 'y'

        password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
        print(f"\n✅ Generated Password: {password}\n")

    except ValueError as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()
