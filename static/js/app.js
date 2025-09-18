(function () {
    const bookingState = {
        selectedService: null,
        selectedDate: null,
        selectedTime: null,
        currentStep: 1
    };

    window.bookingState = bookingState;

    function showToast(message, type = 'success') {
        const container = document.getElementById('toast-container');
        if (!container) {
            return;
        }

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        container.appendChild(toast);

        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }

    window.showToast = showToast;

    window.handleSearchInput = function handleSearchInput(value) {
        if (typeof value !== 'string') {
            return;
        }
        const trimmed = value.trim();
        if (trimmed.length >= 2) {
            window.location.href = `/search?q=${encodeURIComponent(trimmed)}`;
        }
    };

    window.openBookingModalForBusiness = function openBookingModalForBusiness(businessId) {
        if (!businessId) {
            showToast('שגיאה בזיהוי העסק', 'error');
            return;
        }

        fetch(`/api/get-business/${businessId}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Failed to load business data');
                }
                return response.json();
            })
            .then((business) => {
                openBookingModal(business);
            })
            .catch((error) => {
                console.error('Error fetching business:', error);
                showToast('שגיאה בטעינת נתוני העסק', 'error');
            });
    };

    function openBookingModal(business) {
        const modal = document.getElementById('booking-modal');
        const businessName = document.getElementById('booking-business-name');
        const dateInput = document.getElementById('booking-date');

        if (!modal || !businessName) {
            return;
        }

        window.currentBookingBusiness = business;
        businessName.textContent = `הזמנת תור ב${business.name}`;
        modal.classList.add('active');

        bookingState.selectedService = null;
        bookingState.selectedTime = null;
        bookingState.currentStep = 1;
        if (dateInput) {
            bookingState.selectedDate = dateInput.value;
        }

        document.querySelectorAll('.service-item').forEach((item) => {
            item.classList.remove('selected');
        });
        document.querySelectorAll('.time-slot').forEach((slot) => {
            slot.classList.remove('selected');
        });

        loadBookingServices(business.services || []);
        showBookingStep(1);
codex/fix-errors-and-correct-code-f6tn0t
        attachTimeSlotListeners();

    }

    function loadBookingServices(services) {
        const container = document.getElementById('services-list');
        if (!container) {
            return;
        }

        container.innerHTML = '';

        if (!services.length) {
            const emptyState = document.createElement('div');
            emptyState.className = 'service-item empty';
            emptyState.textContent = 'אין שירותים זמינים להצגה';
            container.appendChild(emptyState);
            return;
        }

        services.forEach((service) => {
            const item = document.createElement('div');
            item.className = 'service-item';
            item.addEventListener('click', () => selectService(service, item));
            item.innerHTML = `
                <div class="service-info">
                    <div class="service-name">${service.name}</div>
                    <div class="service-duration">${service.duration} דקות</div>
                </div>
                <div class="service-price">₪${service.price}</div>
            `;
            container.appendChild(item);
        });
    }

    function selectService(service, element) {
        document.querySelectorAll('.service-item').forEach((item) => {
            item.classList.remove('selected');
        });

        element.classList.add('selected');
        bookingState.selectedService = service;
    }

    function showBookingStep(step) {
        const nextStep = document.getElementById(`step-${step}`);
        if (!nextStep) {
            return;
        }

        document.querySelectorAll('.booking-step').forEach((section) => {
            section.classList.add('hidden');
        });
        nextStep.classList.remove('hidden');

        const prevBtn = document.getElementById('prev-step');
        const nextBtn = document.getElementById('next-step');
        const confirmBtn = document.getElementById('confirm-booking');

        if (step === 1) {
            if (prevBtn) prevBtn.classList.add('hidden');
            if (nextBtn) nextBtn.classList.remove('hidden');
            if (confirmBtn) confirmBtn.classList.add('hidden');
        } else if (step === 2) {
            if (prevBtn) prevBtn.classList.remove('hidden');
            if (nextBtn) nextBtn.classList.remove('hidden');
            if (confirmBtn) confirmBtn.classList.add('hidden');
        } else if (step === 3) {
            if (prevBtn) prevBtn.classList.remove('hidden');
            if (nextBtn) nextBtn.classList.add('hidden');
            if (confirmBtn) confirmBtn.classList.remove('hidden');
            loadBookingSummary();
        }

        bookingState.currentStep = step;
    }

    function loadBookingSummary() {
        const container = document.getElementById('booking-summary');
        const dateInput = document.getElementById('booking-date');
        if (!container || !window.currentBookingBusiness) {
            return;
        }

        const dateValue = bookingState.selectedDate || (dateInput ? dateInput.value : '');
        let formattedDate = '';

        if (dateValue) {
            bookingState.selectedDate = dateValue;
            const parsedDate = new Date(dateValue);
            if (!Number.isNaN(parsedDate.getTime())) {
                formattedDate = parsedDate.toLocaleDateString('he-IL', {
                    weekday: 'long',
                    day: 'numeric',
                    month: 'long'
                });
            }
        }

        container.innerHTML = `
            <div class="summary-item">
                <span>עסק:</span>
                <span>${window.currentBookingBusiness.name}</span>
            </div>
            <div class="summary-item">
                <span>שירות:</span>
                <span>${bookingState.selectedService ? bookingState.selectedService.name : ''}</span>
            </div>
            <div class="summary-item">
                <span>תאריך:</span>
                <span>${formattedDate}</span>
            </div>
            <div class="summary-item">
                <span>שעה:</span>
                <span>${bookingState.selectedTime || ''}</span>
            </div>
            <div class="summary-item">
                <span>מחיר:</span>
                <span>₪${bookingState.selectedService ? bookingState.selectedService.price : 0}</span>
            </div>
        `;
    }

    function confirmBooking() {
        if (!window.currentBookingBusiness || !bookingState.selectedService) {
            showToast('אנא בחר שירות לפני האישור', 'error');
            return;
        }

        if (!bookingState.selectedDate || !bookingState.selectedTime) {
            showToast('אנא בחר תאריך ושעה', 'error');
            return;
        }

        const bookingData = {
            business_id: window.currentBookingBusiness.id,
            service_id: bookingState.selectedService.id,
            date: bookingState.selectedDate,
            time: bookingState.selectedTime
        };

        fetch('/api/book-appointment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookingData)
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    showToast(data.message, 'success');
                    const modalElement = document.getElementById('booking-modal');
                    if (modalElement) {
                        modalElement.classList.remove('active');
                    }
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showToast(data.message || 'שגיאה בהזמנת התור', 'error');
                }
            })
            .catch((error) => {
                console.error('Error booking appointment:', error);
                showToast('שגיאה בהזמנת התור', 'error');
            });
    }

    window.cancelAppointment = function cancelAppointment(appointmentId) {
        if (!appointmentId) {
            return;
        }

        fetch('/api/cancel-appointment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ appointment_id: appointmentId })
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    showToast(data.message, 'success');
                    setTimeout(() => window.location.reload(), 800);
                } else {
                    showToast(data.message || 'שגיאה בביטול התור', 'error');
                }
            })
            .catch((error) => {
                console.error('Error cancelling appointment:', error);
                showToast('שגיאה בביטול התור', 'error');
            });
    };

    window.copyReferralCode = function copyReferralCode(code) {
        if (!code) {
            return;
        }

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(code)
                .then(() => showToast('הקוד הועתק בהצלחה', 'success'))
                .catch(() => showToast('לא הצלחנו להעתיק, נסה שוב', 'error'));
        } else {
            const tempInput = document.createElement('input');
            tempInput.value = code;
            document.body.appendChild(tempInput);
            tempInput.select();
            document.execCommand('copy');
            document.body.removeChild(tempInput);
            showToast('הקוד הועתק בהצלחה', 'success');
        }
    };

    window.shareReferralCode = function shareReferralCode(code) {
        if (navigator.share) {
            navigator.share({
                title: 'TORIM',
                text: `מצטרף אלי ל-TORIM! השתמש בקוד ${code} וקבל הטבה.`
            }).catch(() => {
                copyReferralCode(code);
            });
        } else {
            copyReferralCode(code);
        }
    };

    function appendChatMessage(message) {
        const container = document.getElementById('chat-messages');
        if (!container || !message || !message.text) {
            return;
        }

        const wrapper = document.createElement('div');
        wrapper.className = `chat-message ${message.type || 'assistant'}`;

        const content = document.createElement('div');
        content.className = 'message-content';

        const text = document.createElement('p');
        text.textContent = message.text;

        const time = document.createElement('span');
        time.className = 'message-time';
        time.textContent = message.time || new Date().toLocaleTimeString('he-IL', {
            hour: '2-digit',
            minute: '2-digit'
        });

        content.appendChild(text);
        content.appendChild(time);
        wrapper.appendChild(content);
        container.appendChild(wrapper);
        scrollChatToBottom();
    }

    function scrollChatToBottom() {
        const container = document.getElementById('chat-messages');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }

    function handleChatSubmit(event) {
        event.preventDefault();
        const input = document.getElementById('chat-message');
        if (!input) {
            return;
        }

        const value = input.value.trim();
        if (!value) {
            return;
        }

        appendChatMessage({
            type: 'user',
            text: value,
            time: new Date().toLocaleTimeString('he-IL', { hour: '2-digit', minute: '2-digit' })
        });
        input.value = '';

        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: value })
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success && data.message) {
                    appendChatMessage(data.message);
                } else {
                    showToast(data.message || 'שגיאה בשליחת ההודעה', 'error');
                }
            })
            .catch((error) => {
                console.error('Error sending chat message:', error);
                showToast('שגיאה בשליחת ההודעה', 'error');
            });
    }

    function attachChatEvents() {
        const chatForm = document.getElementById('chat-form');
        if (chatForm) {
            chatForm.addEventListener('submit', handleChatSubmit);
            scrollChatToBottom();
        }
    }

    function attachModalEvents() {
        const closeModal = document.getElementById('close-modal');
        const bookingModal = document.getElementById('booking-modal');
        const nextBtn = document.getElementById('next-step');
        const prevBtn = document.getElementById('prev-step');
        const confirmBtn = document.getElementById('confirm-booking');
        const dateInput = document.getElementById('booking-date');

        if (closeModal) {
            closeModal.addEventListener('click', () => {
                if (bookingModal) {
                    bookingModal.classList.remove('active');
                }
            });
        }

        if (bookingModal) {
            bookingModal.addEventListener('click', (event) => {
                if (event.target === bookingModal) {
                    bookingModal.classList.remove('active');
                }
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                if (bookingState.currentStep === 1) {
                    if (!bookingState.selectedService) {
                        showToast('אנא בחר שירות', 'error');
                        return;
                    }
                    showBookingStep(2);
                } else if (bookingState.currentStep === 2) {
                    if (!bookingState.selectedDate || !bookingState.selectedTime) {
                        showToast('אנא בחר תאריך ושעה', 'error');
                        return;
                    }
                    showBookingStep(3);
                }
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                if (bookingState.currentStep > 1) {
                    showBookingStep(bookingState.currentStep - 1);
                }
            });
        }

        if (confirmBtn) {
            confirmBtn.addEventListener('click', confirmBooking);
        }

        if (dateInput) {
            dateInput.addEventListener('change', (event) => {
                bookingState.selectedDate = event.target.value;
            });
        }
    }

    function attachTimeSlotListeners() {
        document.querySelectorAll('.time-slot').forEach((slot) => {
            if (slot.dataset.bound === 'true') {
                return;
            }


            slot.addEventListener('click', () => {
                document.querySelectorAll('.time-slot').forEach((item) => item.classList.remove('selected'));
                slot.classList.add('selected');
                bookingState.selectedTime = slot.textContent;
            });
 codex/fix-errors-and-correct-code-f6tn0t

            slot.dataset.bound = 'true';
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.style.display = 'none';
        }

        attachModalEvents();
        attachTimeSlotListeners();
        attachChatEvents();
    });
})();
