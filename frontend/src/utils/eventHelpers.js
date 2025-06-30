/**
 * This file contains utilities to help prevent common issues with form interactions
 * that can lead to page reloads or flashes in the Job Tracker application.
 */

/**
 * Create a synthetic event handler that prevents default behavior and stops propagation.
 * This helps avoid unintentional form submissions from control elements.
 * 
 * @param {Function} handler - The event handler function to wrap
 * @returns {Function} A wrapped handler that prevents page reloads
 */
export const createSafeEventHandler = (handler) => {
  return (event) => {
    // Always prevent default browser behavior first
    if (event && event.preventDefault) {
      event.preventDefault();
    }
    
    // Stop event propagation to parent elements
    if (event && event.stopPropagation) {
      event.stopPropagation();
    }
    
    // Call the original handler
    return handler(event);
  };
};

/**
 * Utility to safely update a state value while preventing page reloads.
 * Useful for filter components that might cause page refreshes.
 * 
 * @param {Function} setter - The state setter function 
 * @returns {Function} A safe handler for updating state
 */
export const createSafeStateSetter = (setter) => {
  return (value) => {
    // If it's an event, extract the value
    if (value && value.target) {
      const targetValue = value.target.type === 'checkbox' 
        ? value.target.checked 
        : value.target.value;
      
      // Prevent form submission
      if (value.preventDefault) {
        value.preventDefault();
        value.stopPropagation();
      }
      
      // Call the setter with the extracted value
      setter(targetValue);
    } else {
      // Just a regular value, pass it through
      setter(value);
    }
  };
};

/**
 * Apply form-prevention attributes to a DOM element.
 * This is useful for ensuring that buttons don't trigger form submissions.
 * 
 * @param {Object} props - The props object to enhance
 * @returns {Object} Enhanced props with form-prevention attributes
 */
export const preventFormSubmission = (props = {}) => {
  return {
    ...props,
    type: 'button', // Ensure it's not a submit button
    onClick: props.onClick ? createSafeEventHandler(props.onClick) : undefined,
    // Add the novalidate attribute to prevent HTML5 validation
    formNoValidate: true,
    // Prevent default actions on mouse events
    onMouseDown: (e) => e.preventDefault()
  };
};

/**
 * Global form prevention utility to add to the app's root component.
 * This prevents all default form submissions in the application.
 * 
 * @returns {Function} An event handler for the onSubmit event
 */
export const preventAllFormSubmissions = (e) => {
  // Check if this is a form submission or an intentional button click
  if (e && e.target && (
    // Only prevent default for unintentional form submissions
    (e.type === 'submit' && !e._isIntentional) || 
    // Or for buttons that might cause page navigation but shouldn't
    (e.type === 'click' && 
     e.target.tagName === 'BUTTON' && 
     !e.target.type && 
     !e.target.closest('form'))
  )) {
    e.preventDefault();
    e.stopPropagation();
    console.warn('Prevented unintentional form submission or navigation.');
    return false;
  }
  
  // Let intentional submissions through
  return true;
};
