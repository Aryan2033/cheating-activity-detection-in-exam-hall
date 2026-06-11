from django.shortcuts import render
from urllib import request
from django.http import  JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.
from .models import newuser,PredictedImage,Contact



def navbar(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        desc=request.POST['desc']
        contacts= Contact(name=name,email=email,phone=phone,desc=desc)
        contacts.save()    
        return redirect('contact')
    else:
        return render(request, 'contact.html')


def user_contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        desc=request.POST['desc']
        contacts= Contact(name=name,email=email,phone=phone,desc=desc)
        contacts.save()    
        return redirect('user_contact')
    else:
        return render(request, 'user_contact.html')
    


def login(request):
    if request.method== 'POST':
        try:
            Userdetailes=newuser.objects.get(Username=request.POST['Username'], pass1=request.POST['pass1'])
            print("Username=",Userdetailes)
            request.session['Username']=Userdetailes.Username
            messages.success(request,"successfully login")
            return redirect('userhome')
        except newuser.DoesNotExist as e:   
            messages.error(request,"Username/ Password Invalied...!")
   
    return render(request,'login.html')


def registration(request):
    if request.method == 'POST':
        Username=request.POST['Username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if newuser.objects.filter(Username=Username).exists():
            messages.warning(request,'Username is already exists')
            return redirect('registration')
        else:
            newuser(Username=Username, fname=fname, lname=lname, email=email, pass1=pass1, pass2=pass2).save()
            messages.success(request, 'The new user '+request.POST['Username']+ " IS saved successfully..!")
            return redirect('login')
    else:
         return render(request,'registration.html')


def logout(request):
    # logout(request)
    messages.success(request,"successfully logout..!")
    return redirect('navbar')


def userhome(request):
    return render(request,'userhome.html')




def admin_login(request):
    if request.method== 'POST':
        try:
            Userdetailes=newuser.objects.get(Username=request.POST['Username'], pass1=request.POST['pass1'])
            print("Username=",Userdetailes)
            request.session['Username']=Userdetailes.Username
            messages.success(request,"successfully login")
            return redirect('admin_home')
        except newuser.DoesNotExist as e:   
            messages.error(request,"Username/ Password Invalied...!")
   
    return render(request,'admin_login.html')


def admin_registration(request):
    if request.method == 'POST':
        Username=request.POST['Username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if newuser.objects.filter(Username=Username).exists():
            messages.warning(request,'Username is already exists')
            return redirect('admin_registration')
        else:
            newuser(Username=Username, fname=fname, lname=lname, email=email, pass1=pass1, pass2=pass2).save()
            messages.success(request, 'The new user '+request.POST['Username']+ " IS saved successfully..!")
            return redirect('admin_login')
    else:
         return render(request,'admin_registration.html')


def admin_logout(request):
    # logout(request)
    messages.success(request,"successfully logout..!")
    return redirect('navbar')

def admin_home(request):
    return render(request, 'admin_home.html')



def view_user(request):
    form=newuser.objects.all()
    return render(request,'view_user.html' , {'forms':form})



import os
import cv2
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from ultralytics import YOLO
from .models import VideoUpload
import uuid
import cv2
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import VideoUpload  # Make sure you have this model
from ultralytics import YOLO
def detect_objects_in_video(video_path, output_path):
    from ultralytics import YOLO
    import cv2

    model = YOLO('best (16).pt')
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file:", video_path)
        return []

    fps = cap.get(cv2.CAP_PROP_FPS) or 20.0

    ret, frame = cap.read()
    if not ret:
        print("Error reading video frames")
        return []

    height, width = frame.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    detected_objects = {}

    while ret:
        results = model(frame)[0]
        boxes = results.boxes

        for box in boxes:
            bb = box.xyxy[0].cpu().numpy().astype(int)
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls_id]
            is_cheating = label.lower() == "cheating"
            box_color = (0, 0, 255) if is_cheating else (0, 255, 0)

            # Draw box and label
            cv2.rectangle(frame, (bb[0], bb[1]), (bb[2], bb[3]), box_color, 3)
            cv2.putText(frame, f"{label} {conf:.2f}", (bb[0], bb[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, box_color, 2)

            if is_cheating:
                cv2.rectangle(frame, (0, 0), (width - 1, height - 1), (0, 0, 255), 12)

            current_best = detected_objects.get(label)
            if current_best is None or conf > current_best["confidence_raw"]:
                detected_objects[label] = {
                    "label": label,
                    "confidence": round(conf * 100, 2),
                    "confidence_raw": conf,
                }

        out.write(frame)
        ret, frame = cap.read()

    cap.release()
    out.release()

    return sorted(
        [
            {"label": item["label"], "confidence": item["confidence"]}
            for item in detected_objects.values()
        ],
        key=lambda item: item["confidence"],
        reverse=True,
    )

def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        import uuid, os
        from django.conf import settings
        from django.core.files.storage import FileSystemStorage
        from .models import VideoUpload

        video = request.FILES['video']
        fs = FileSystemStorage()

        unique_filename = str(uuid.uuid4()) + "_" + video.name
        original_video_path = f"videos/original/{unique_filename}"
        processed_video_path = f"videos/processed/processed_{unique_filename}"

        os.makedirs(os.path.join(settings.MEDIA_ROOT, "videos/original"), exist_ok=True)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, "videos/processed"), exist_ok=True)

        filename = fs.save(original_video_path, video)
        uploaded_video_full_path = fs.path(filename)
        processed_video_full_path = os.path.join(settings.MEDIA_ROOT, processed_video_path)

        # Run detection and get object results
        detected_objects = detect_objects_in_video(uploaded_video_full_path, processed_video_full_path)

        VideoUpload.objects.create(
            original_video=original_video_path,
            processed_video=processed_video_path,
        )

        return render(request, 'result.html', {
            'original_video_url': fs.url(original_video_path),
            'processed_video_url': fs.url(processed_video_path),
            'detected_objects': detected_objects,
        })

    return render(request, 'upload_video.html')









from django.shortcuts import render
from django.http import StreamingHttpResponse
from .models import CheatingDetection
from ultralytics import YOLO
import cv2
import time
import uuid
from django.core.files.base import ContentFile

# Load YOLO model once
model = YOLO("best (16).pt")  



from django.core.mail import EmailMessage
from django.conf import settings
import os

def send_cheating_email(detection):
    """
    Sends an email with detection data and screenshot attachment using Django's EmailMessage.
    """
    subject = "Cheating Screenshot Classification Report"
    body = (
        f"Cheating Detection Report:\n\n"
        f"Detected Class: {detection['class']}\n"
        f"Confidence: {detection['confidence']:.2f}\n"
        f"Timestamp: {detection['timestamp']}\n"
        f"Frame Number: {detection['frame_number']}"
    )

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=["maheshkadam9298@gmail.com"]
    )

    # Attach image
    try:
        with open(detection['image_path'], 'rb') as img:
            email.attach(os.path.basename(detection['image_path']), img.read(), 'image/jpeg')
    except Exception as e:
        print(f"Failed to attach image: {e}")

    try:
        email.send()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")



def run_detection(request):
    return render(request, 'run_detection.html')

def generate_frames():
    video_path = "./dataset/testvideo.mp4"
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    last_saved_second = -1  # Track last second when screenshot was saved

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        cheating_detected = False  # Reset cheating flag

        results = model(frame)

        save_this_frame = False
        best_detection = None

        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    conf = float(box.conf[0].cpu().numpy())
                    cls = int(box.cls[0].cpu().numpy())
                    detected_label = model.names[cls]

                    # Set box color based on label
                    if detected_label.lower() == "cheating":
                        box_color = (0, 0, 255)  # Red for cheating
                    else:
                        box_color = (0, 255, 0)  # Green for other classes

                    # Draw box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                    cv2.putText(frame, f"{detected_label}: {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)

                    # Save screenshot if cheating detected
                    if detected_label.lower() == "cheating" and conf > 0.5:
                        cheating_detected = True

                        seconds = int(frame_count / fps)

                        if seconds > last_saved_second:
                            last_saved_second = seconds
                            save_this_frame = True
                            best_detection = {
                                "timestamp": time.strftime('%H:%M:%S', time.gmtime(seconds)),
                                "detected_label": detected_label,
                                "conf": conf,
                                "frame_number": frame_count,
                                "frame": frame.copy()
                            }

        # Save screenshot and send email
        if save_this_frame and best_detection:
            _, buffer = cv2.imencode('.jpg', best_detection["frame"])
            image_data = ContentFile(buffer.tobytes())
            unique_filename = f"{uuid.uuid4()}.jpg"

            detection = CheatingDetection(
                timestamp=best_detection["timestamp"],
                detected_class=best_detection["detected_label"],
                confidence=best_detection["conf"],
                frame_number=best_detection["frame_number"],
            )
            detection.screenshot.save(unique_filename, image_data, save=True)

            detection_data = {
                'timestamp': best_detection["timestamp"],
                'class': best_detection["detected_label"],
                'confidence': best_detection["conf"],
                'frame_number': best_detection["frame_number"],
                'image_path': detection.screenshot.path
            }
            send_cheating_email(detection_data)

        # Draw red border around frame if cheating detected
        if cheating_detected:
            thickness = 15
            color = (0, 0, 255)  # Red
            frame = cv2.copyMakeBorder(frame, thickness, thickness, thickness, thickness, cv2.BORDER_CONSTANT, value=color)

        # Convert frame and yield
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
