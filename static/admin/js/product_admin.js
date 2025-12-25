// Preserve uploaded images when form validation fails and improve error display
(function($) {
    'use strict';
    
    // Store file inputs in sessionStorage to persist across page reloads
    var fileInputs = {};
    
    $(document).ready(function() {
        // Before form submit, save all file inputs to sessionStorage
        $('form').on('submit', function(e) {
            fileInputs = {};
            $('input[type="file"]').each(function() {
                var input = $(this);
                var name = input.attr('name');
                if (input[0].files && input[0].files.length > 0) {
                    var files = [];
                    for (var i = 0; i < input[0].files.length; i++) {
                        var file = input[0].files[i];
                        var reader = new FileReader();
                        reader.onload = (function(file) {
                            return function(e) {
                                fileInputs[name] = fileInputs[name] || [];
                                fileInputs[name].push({
                                    name: file.name,
                                    type: file.type,
                                    size: file.size,
                                    data: e.target.result
                                });
                                sessionStorage.setItem('fileInputs_' + name, JSON.stringify(fileInputs[name]));
                            };
                        })(file);
                        reader.readAsDataURL(file);
                    }
                }
            });
        });
        
        // After page load, check for errors and restore file previews
        setTimeout(function() {
            if ($('.errorlist').length > 0) {
                // Restore file previews from sessionStorage
                $('input[type="file"]').each(function() {
                    var input = $(this);
                    var name = input.attr('name');
                    var stored = sessionStorage.getItem('fileInputs_' + name);
                    
                    if (stored) {
                        try {
                            var files = JSON.parse(stored);
                            var container = input.closest('.form-row, .field-box, .inline-group, .form-group');
                            
                            files.forEach(function(fileData) {
                                var preview = container.find('.file-preview[data-name="' + name + '"]');
                                if (preview.length === 0) {
                                    preview = $('<div class="file-preview" data-name="' + name + '" style="margin-top: 10px; padding: 10px; background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px;"></div>');
                                    input.after(preview);
                                }
                                
                                if (fileData.type && fileData.type.startsWith('image/')) {
                                    preview.append('<div style="margin-bottom: 5px;"><img src="' + fileData.data + '" style="max-width: 200px; border: 1px solid #ddd; border-radius: 4px;"><br><small style="color: #28a745;">✓ Fajl je sačuvan: ' + fileData.name + ' (' + (fileData.size / 1024).toFixed(2) + ' KB)</small></div>');
                                } else {
                                    preview.append('<div style="margin-bottom: 5px;"><small style="color: #28a745;">✓ Fajl je sačuvan: ' + fileData.name + ' (' + (fileData.size / 1024).toFixed(2) + ' KB)</small></div>');
                                }
                            });
                            
                            // Add note that file is preserved
                            container.find('.file-preview').append('<div style="margin-top: 5px; color: #856404; font-size: 12px;"><strong>Napomena:</strong> Fajl je sačuvan i neće biti obrisan. Možete nastaviti sa popravkom grešaka.</div>');
                        } catch(e) {
                            console.error('Error restoring file:', e);
                        }
                    }
                });
                
                // Clear sessionStorage after successful save
                $('form').on('submit', function() {
                    if ($('.errorlist').length === 0) {
                        sessionStorage.clear();
                    }
                });
            }
            
            // Better error display - highlight fields with errors
            $('.errorlist').each(function() {
                var errorList = $(this);
                var field = errorList.closest('.form-row, .field-box, .inline-group, .form-group');
                if (field.length) {
                    field.addClass('has-error');
                }
                
                // Also highlight the input field itself
                var input = field.find('input, textarea, select');
                if (input.length) {
                    input.addClass('error');
                }
            });
            
            // Scroll to first error
            if ($('.errorlist').length > 0) {
                $('html, body').animate({
                    scrollTop: $('.errorlist').first().offset().top - 100
                }, 500);
            }
        }, 100);
    });
})(django.jQuery || jQuery);

