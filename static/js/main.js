// Main JavaScript file for Centro Veterinario

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling para enlaces internos
    initSmoothScrolling();
    
    // Animaciones de aparición al hacer scroll
    initScrollAnimations();
    
    // Validación de formulario en tiempo real
    initFormValidation();
    
    // Navegación activa
    initActiveNavigation();
    
    // Contador de estadísticas (si existe)
    initStatisticsCounter();
    
    // Modal de confirmación para citas
    initAppointmentModal();
});

// Smooth scrolling para enlaces internos
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Animaciones de aparición al hacer scroll
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // Elementos a observar
    const elementsToObserve = [
        '.feature-card',
        '.service-item',
        '.service-card',
        '.additional-service-item',
        '.clinic-info'
    ];

    elementsToObserve.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            observer.observe(el);
        });
    });
}

// Validación de formulario en tiempo real
function initFormValidation() {
    const form = document.querySelector('.appointment-form-content');
    if (!form) return;

    const inputs = form.querySelectorAll('.form-control');
    
    inputs.forEach(input => {
        // Validación al perder el foco
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        // Validación al escribir
        input.addEventListener('input', function() {
            if (this.classList.contains('error')) {
                validateField(this);
            }
        });
    });

    // Validación al enviar el formulario
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showNotification('Por favor, completa todos los campos correctamente.', 'error');
        }
    });
}

// Validar campo individual
function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    
    // Remover clases de error previas
    field.classList.remove('error');
    
    // Validaciones específicas
    if (field.type === 'date') {
        const selectedDate = new Date(value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate < today) {
            isValid = false;
            showFieldError(field, 'La fecha no puede ser anterior a hoy');
        }
    }
    
    if (field.type === 'time') {
        const time = value.split(':');
        const hour = parseInt(time[0]);
        
        if (hour < 8 || hour > 20) {
            isValid = false;
            showFieldError(field, 'Horario disponible: 8:00 AM - 8:00 PM');
        }
    }
    
    // Validación general de campo requerido
    if (!value) {
        isValid = false;
        showFieldError(field, 'Este campo es requerido');
    }
    
    return isValid;
}

// Mostrar error en campo específico
function showFieldError(field, message) {
    field.classList.add('error');
    
    // Remover mensaje de error previo
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Crear mensaje de error
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.color = 'var(--error-color)';
    errorDiv.style.fontSize = '0.75rem';
    errorDiv.style.marginTop = '0.25rem';
    
    field.parentNode.appendChild(errorDiv);
}

// Navegación activa
function initActiveNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Contador de estadísticas (animación)
function initStatisticsCounter() {
    const counters = document.querySelectorAll('.statistic-counter');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'));
                const duration = 2000; // 2 segundos
                const increment = target / (duration / 16); // 60fps
                let current = 0;
                
                const updateCounter = () => {
                    current += increment;
                    if (current < target) {
                        counter.textContent = Math.floor(current);
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target;
                    }
                };
                
                updateCounter();
                observer.unobserve(counter);
            }
        });
    });
    
    counters.forEach(counter => observer.observe(counter));
}

// Modal de confirmación para citas
function initAppointmentModal() {
    const form = document.querySelector('.appointment-form-content');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Recopilar datos del formulario
        const formData = new FormData(this);
        const appointmentData = {
            mascota: formData.get('txtMascota'),
            fecha: formData.get('txtFecha'),
            hora: formData.get('txtHora')
        };
        
        // Mostrar modal de confirmación
        showConfirmationModal(appointmentData, () => {
            // Enviar formulario después de confirmación
            this.submit();
        });
    });
}

// Mostrar modal de confirmación
function showConfirmationModal(data, onConfirm) {
    const modal = document.createElement('div');
    modal.className = 'confirmation-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-calendar-check"></i> Confirmar Cita</h3>
                <button class="modal-close">&times;</button>
            </div>
            <div class="modal-body">
                <p>¿Confirmas la cita para <strong>${data.mascota}</strong>?</p>
                <div class="appointment-details">
                    <p><i class="fas fa-calendar"></i> Fecha: ${formatDate(data.fecha)}</p>
                    <p><i class="fas fa-clock"></i> Hora: ${formatTime(data.hora)}</p>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" id="cancel-appointment">Cancelar</button>
                <button class="btn btn-primary" id="confirm-appointment">Confirmar Cita</button>
            </div>
        </div>
    `;
    
    // Estilos del modal
    const styles = `
        <style>
            .confirmation-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                animation: fadeIn 0.3s ease;
            }
            
            .modal-content {
                background: white;
                border-radius: 1rem;
                padding: 2rem;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
                animation: slideIn 0.3s ease;
            }
            
            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1.5rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid var(--border-color);
            }
            
            .modal-header h3 {
                margin: 0;
                color: var(--text-dark);
            }
            
            .modal-close {
                background: none;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                color: var(--text-light);
            }
            
            .modal-body {
                margin-bottom: 1.5rem;
            }
            
            .appointment-details {
                background: var(--light-gray);
                padding: 1rem;
                border-radius: 0.5rem;
                margin-top: 1rem;
            }
            
            .appointment-details p {
                margin: 0.5rem 0;
                color: var(--text-dark);
            }
            
            .modal-footer {
                display: flex;
                gap: 1rem;
                justify-content: flex-end;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes slideIn {
                from { transform: translateY(-50px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
        </style>
    `;
    
    document.head.insertAdjacentHTML('beforeend', styles);
    document.body.appendChild(modal);
    
    // Event listeners
    modal.querySelector('.modal-close').addEventListener('click', () => {
        modal.remove();
    });
    
    modal.querySelector('#cancel-appointment').addEventListener('click', () => {
        modal.remove();
    });
    
    modal.querySelector('#confirm-appointment').addEventListener('click', () => {
        modal.remove();
        onConfirm();
    });
    
    // Cerrar modal al hacer clic fuera
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

// Mostrar notificación
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button class="notification-close">&times;</button>
    `;
    
    // Estilos de notificación
    const styles = `
        <style>
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 1rem 1.5rem;
                border-radius: 0.5rem;
                color: white;
                font-weight: 500;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                z-index: 10001;
                animation: slideInRight 0.3s ease;
                max-width: 400px;
            }
            
            .notification-success {
                background: var(--success-color);
            }
            
            .notification-error {
                background: var(--error-color);
            }
            
            .notification-info {
                background: var(--primary-color);
            }
            
            .notification-close {
                background: none;
                border: none;
                color: white;
                font-size: 1.25rem;
                cursor: pointer;
                margin-left: auto;
            }
            
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        </style>
    `;
    
    if (!document.querySelector('#notification-styles')) {
        const styleElement = document.createElement('style');
        styleElement.id = 'notification-styles';
        styleElement.textContent = styles;
        document.head.appendChild(styleElement);
    }
    
    document.body.appendChild(notification);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
    
    // Cerrar manualmente
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.remove();
    });
}

// Utilidades
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
}

// Lazy loading para imágenes
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Inicializar lazy loading si hay imágenes
if (document.querySelectorAll('img[data-src]').length > 0) {
    initLazyLoading();
} 