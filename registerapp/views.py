from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password, make_password
from requests import session
from registerapp.models import User  # Import your custom User model
import logging
from datetime import datetime
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from .models import User  # Ensure your User model is imported
# Registration view
def register(request):
    if request.method == "POST":
        first_name = request.POST.get('FitFusion.ai_user_first_name')
        last_name = request.POST.get('FitFusion.ai_user_last_name')
        email = request.POST.get('FitFusion.ai_user_email')
        contact_number = request.POST.get('FitFusion.ai_user_contact_number')
        password = request.POST.get('FitFusion.ai_user_password')
        confirm_password = request.POST.get('FitFusion.ai_user_confirm_password')
        newsletter_signup = 'FitFusion.ai_newsletter_signup' in request.POST  # Checkbox data

        # Validate password match
        if password != confirm_password:
            return HttpResponse("Error: Passwords do not match.", status=400)

        # Prepare data for user creation
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'contact_number': contact_number,
            'password': make_password(password),  # The save method will hash it
            'newsletter_signup': newsletter_signup
        }
        print(f"Email: {email}, Password: {password}, Contact Number: {contact_number}, First Name: {first_name}, Last Name: {last_name}")
        print(User._meta.get_fields())

        # Try to create the user and save to the database
        try:
            user = User(**data)  # Create user instance
            user.save()  # Save with hashed password (handled by model's save method)
            print(f"User created: {user}")
            return redirect('signinPage')  # Redirect to login page after successful registration
        except Exception as e:
            print(f"Error creating user: {e}")
            return HttpResponse(f"Error: {str(e)}", status=400)

    # If the method is not POST, render the registration form
    return render(request, 'sign-up.html')

def authenticate_user(email, password):
    if not email or not password:
        return "Error: Missing email or password."
    
    email = email.lower()  # Normalize to lowercase
    
    try:
        user = User.objects.get(email=email)  # Get the user by email
        # Debugging: Printing user information (not ideal in production)
        print("----")
        print(user)
        print("----")
        print(user.password)  # This is the hashed password in the database
        print(password)  # The plain password entered by the use
        # Check if the provided password matches the hashed password in the database
        if check_password(password, user.password):
            print("-----")
            print(check_password(password, user.password))
            return user  # Return the user object if password matches
        else:
            return "Error: Invalid password."  # Password mismatch

    except User.DoesNotExist:
        return "Error: User not found with that email."  # User not found with that email
    except Exception as e:
        return f"An unexpected error occurred during login: {str(e)}" 

# Login view
def login(request):
    if request.method == "POST":
        email = request.POST.get('FitFusion.ai_user_email')
        password = request.POST.get('FitFusion.ai_user_password')
        
        # Print the email and password for debugging
        print(f"Email: {email}, Password: {password}")
        
        # Use custom authenticate_user function
        user = authenticate_user(email, password)
        print(user)
        if isinstance(user, User):  # If authenticate_user returns a User object
            auth_login(request, user)  # Log the user in
            request.session['user_name'] = user.first_name
            request.session['user_id'] = user.id
            print(f"User name stored in session: {request.session['user_name'], request.session['user_id']}")
            print(f"Session data after login: {request.session.items()}")
            print(session)
            return redirect('homePage2')  # Redirect to home page after successful login
          

            
        else:
            return HttpResponse(user, status=400)  # Return the error message from authenticate_user

    # If the method is not POST, render the login form
    return render(request, 'sign-in.html')
#@login_required
def updatepassword(request):
    user_id = request.session.get('user_id')  # Get user ID from session
    user_name = request.session.get('user_name')  # Get username from session
    if not user_id:  
        return HttpResponse("Error: User not logged in.", status=401)

    try:
        user = User.objects.get(id=user_id)  # Fetch user data from database
    except User.DoesNotExist:
        return HttpResponse("Error: User not found.", status=404)
  

    if request.method == "POST":
        old_password = request.POST.get('FitFusion.ai_user_old_password')
        new_password = request.POST.get('FitFusion.ai_user_new_password')
        confirm_password = request.POST.get('FitFusion.ai_user_confirm_password')

        print(f"Old Password: {old_password}, New Password: {new_password}, Confirm Password: {confirm_password}")

        # Validate old password
        if not check_password(old_password, user.password):
            print("old password incorrect")
            messages.error(request, "Error: Old password is incorrect.")
            return render(request, 'changepassword.html', {'user': user, 'user_name': user_name})

        # Validate new password match
        if new_password != confirm_password:
            print("new password do not match")
            messages.error(request, "Error: New passwords do not match.")
            return render(request, 'changepassword.html', {'user': user, 'user_name': user_name})

        # Update password
        try:
            print("------")
            user.password = make_password(new_password)  # Correct method
            user.save()
            print(f"Updated Hashed Password: {user.password}")  # Debugging


            # Maintain session authentication after password change
            update_session_auth_hash(request, user)

            messages.success(request, "Your password has been updated successfully.")
            return redirect('profilePage')  # Redirect to profile after success

        except Exception as e:
            print(f"Error updating password: {str(e)}")
            messages.error(request, "Error updating password.")
            return render(request, 'changepassword.html', {'user': user})

    # Render change password page if not a POST request
    return render(request, 'changepassword.html', {'user': user, 'user_name': user_name})

def homePage(request):
    # Get the user's name from the session
    user_name = request.session.get('user_name', None)  # Default to 'Guest' if no name in session
    print(f"User name from session: {user_name}")
    return render(request, 'homePage2', {'user_name': user_name})

def logout(request):
    # Clear the user_name session variable
    if 'user_name' in request.session:
        del request.session['user_name']
    
    # Log out the user and redirect to the home page or login page
    auth_logout(request)
    return redirect('homePage')

#@login_required
def updateprofile(request):
    print("-------")
    user_name=request.session['user_name']
    user = User.objects.get(id= request.session['user_id'])  # Get the logged-in user

    if request.method == "POST":
        # Retrieve the updated data from the form
      
        gender = request.POST.get('FitFusion.ai_user_gender')
        height = request.POST.get('FitFusion.ai_user_height')
        weight = request.POST.get('FitFusion.ai_user_weight')
        dob = request.POST.get('FitFusion.ai_user_dob')
        goal = request.POST.get('FitFusion.ai_user_goal')
        target_areas = request.POST.get('FitFusion.ai_user_target_areas')
        workout_experience = request.POST.get('FitFusion.ai_user_workout_experience')
        diet_preferences = request.POST.get('FitFusion.ai_user_diet_preferences')
        medical_conditions = request.POST.get('FitFusion.ai_user_medical_conditions')
        profile_image = request.FILES.get('FitFusion.ai_user_profile_image')  # Handle profile image upload

        # Ensure the form allows file uploads
        if not profile_image:
            messages.error(request, "Error: Profile image is required.")
            return render(request, 'updateprofilepage.html', {'user': user, 'user_name': user_name})
            return HttpResponse("Error: Profile image is required.", status=400) 

        # Convert height and weight to integers if they are provided
        try:
            height = int(height) if height and height.isdigit() else None
            weight = int(weight) if weight and weight.isdigit() else None
        except ValueError:
            return HttpResponse("Error: Height and Weight must be valid numbers.", status=400)

        # Convert dob to date if provided
        if dob:
            try:
                dob = datetime.strptime(dob, "%Y-%m-%d").date()  # Convert the string date to date object
            except ValueError:
                return HttpResponse("Error: Invalid Date of Birth format.", status=400)

        # Prepare data to update the user's profile
        user.gender = gender
        user.height = height
        user.weight = weight
        user.dob = dob
        user.goal = goal
        user.target_areas = target_areas
        user.workout_experience = workout_experience
        user.diet_preferences = diet_preferences
        user.medical_conditions = medical_conditions

        # Only update the profile image if a new one is provided
        if profile_image:
            user.profile_image = profile_image

        # Try to save the updated user data
        try:
            user.save()  # Save updated data to the database
            print(f"User updated: {user}")
            return redirect('profilePage')  # Redirect to the user's profile page after successful update
        except Exception as e:
            print(f"Error updating user: {e}")
            return HttpResponse(f"Error: {str(e)}", status=400)

    # If the method is not POST, render the profile update form with existing data
    return render(request, 'updateprofilepage.html', {'user': user,'user_name': user_name})


def profile(request):
    user_id = request.session.get('user_id')  # Get user ID from session
    user_name = request.session.get('user_name')  # Get username from session

    if not user_id:  
        return HttpResponse("Error: User not logged in.", status=401)

    try:
        user = User.objects.get(id=user_id)  # Fetch user data from database
    except User.DoesNotExist:
        return HttpResponse("Error: User not found.", status=404)

    if request.method == "POST":
        # Fetch updated data from form
        gender = request.POST.get('FitFusion.ai_user_gender')
        height = request.POST.get('FitFusion.ai_user_height')
        weight = request.POST.get('FitFusion.ai_user_weight')
        dob = request.POST.get('FitFusion.ai_user_dob')
        goal = request.POST.get('FitFusion.ai_user_goal')
        target_areas = request.POST.get('FitFusion.ai_user_target_areas')
        workout_experience = request.POST.get('FitFusion.ai_user_workout_experience')
        diet_preferences = request.POST.get('FitFusion.ai_user_diet_preferences')
        medical_conditions = request.POST.get('FitFusion.ai_user_medical_conditions')
        profile_image = request.FILES.get('FitFusion.ai_user_profile_image')

        # Convert height and weight to numbers
        try:
            height = int(height) if height else None
            weight = int(weight) if weight else None
        except ValueError:
            return HttpResponse("Error: Height and Weight must be valid numbers.", status=400)

        # Convert dob to a date object
        if dob:
            try:
                dob = datetime.strptime(dob, "%Y-%m-%d").date()
            except ValueError:
                return HttpResponse("Error: Invalid Date of Birth format.", status=400)

        # Update user attributes
        user.gender = gender
        user.height = height
        user.weight = weight
        user.dob = dob
        user.goal = goal
        user.target_areas = target_areas
        user.workout_experience = workout_experience
        user.diet_preferences = diet_preferences
        user.medical_conditions = medical_conditions

        if profile_image:
            user.profile_image = profile_image  # Update profile image only if a new one is uploaded

        try:
            user.save()
            return redirect('profilePage')  # Redirect to profile page after update
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=400)

    # Render profile update page with user data
    return render(request, 'profilepage.html', {'user': user, 'user_name': user_name})
