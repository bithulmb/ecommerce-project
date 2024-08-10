document.addEventListener('DOMContentLoaded', function () {
    var thumbnailInput = document.getElementById('thumbnail-input');
    var imagePreview = document.getElementById('image-preview');
    var cropperContainer = document.getElementById('cropper-container');
    var imageCropper = document.getElementById('image-cropper');
    var cropper;

    thumbnailInput.addEventListener('change', function (event) {
        var files = event.target.files;
        var done = function (url) {
            thumbnailInput.value = '';
            imageCropper.src = url;
            imagePreview.style.display = 'none';
            cropperContainer.style.display = 'block';

            if (cropper) {
                cropper.destroy();
            }
            cropper = new Cropper(imageCropper, {
                aspectRatio: 1,
                viewMode: 2,
                crop(event) {
                    // You can get the crop box data here if needed
                }
            });
        };
        
        if (files && files.length > 0) {
            var reader = new FileReader();
            reader.onload = function (event) {
                done(reader.result);
            };
            reader.readAsDataURL(files[0]);
        }
    });

    var form = document.getElementById('product-variant-form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        if (cropper) {
            cropper.getCroppedCanvas().toBlob(function (blob) {
                var formData = new FormData(form);
                formData.append('thumbnail', blob, 'cropped_thumbnail.png');

                // Send the form data via AJAX
                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.text())
                .then(data => {
                    // Handle the response here
                    console.log('Success:', data);
                    window.location.href = "{% url 'admin_product_variants' %}"; // Redirect after success
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        }
    });
});
