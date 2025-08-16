import React, { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';
import axios from 'axios';
import { 
  QuestionMarkCircleIcon, 
  InformationCircleIcon 
} from '@heroicons/react/24/outline';

const JobDescriptionEntry = () => {
  // Initial form state
  const initialFormState = {
    jd_title: '',
    primary_skill: '',
    secondary_skills: '',
    mode: '',
    tenure_months: '',
    open_positions: '',
    available_positions: '',
    experience_min: '',
    experience_max: '',
    budget_min: '',
    budget_max: '',
    jd_keywords: '',
    original_jd: '',
    special_instruction: ''
  };

  const [formData, setFormData] = useState(initialFormState);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Clear form data on page reload/component mount
  useEffect(() => {
    console.log('Component mounted - clearing form data');
    
    // Check if this is a page reload
    const isReload = window.performance.navigation.type === 1;
    console.log('Is page reload?', isReload);
    
    // Check if page is visible (might be hidden due to browser behavior)
    const isVisible = !document.hidden;
    console.log('Is page visible?', isVisible);
    
    // Force clear form data
    setFormData(initialFormState);
    setErrors({});
    setIsSubmitting(false);
    
    // Additional check after a short delay
    setTimeout(() => {
      console.log('Delayed form clear check');
      if (JSON.stringify(formData) !== JSON.stringify(initialFormState)) {
        console.log('Form data still not cleared, forcing again');
        setFormData(initialFormState);
        setErrors({});
        setIsSubmitting(false);
      }
    }, 200);
    
  }, []);

  // Additional event listeners for page reload
  useEffect(() => {
    const handleBeforeUnload = () => {
      console.log('Page is about to reload - clearing form data');
      // Clear any stored form data
      localStorage.removeItem('jdFormData');
      sessionStorage.removeItem('jdFormData');
    };

    const handleLoad = () => {
      console.log('Page loaded - ensuring form is clear');
      setFormData(initialFormState);
      setErrors({});
      setIsSubmitting(false);
    };

    // Handle visibility change (when user switches tabs and comes back)
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        console.log('Page became visible - checking form state');
        setFormData(initialFormState);
        setErrors({});
        setIsSubmitting(false);
      }
    };

    // Add event listeners
    window.addEventListener('beforeunload', handleBeforeUnload);
    window.addEventListener('load', handleLoad);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    // Handle page show event (specifically for page reloads)
    const handlePageShow = (event) => {
      console.log('Page show event triggered', event);
      if (event.persisted) {
        console.log('Page was loaded from cache - forcing form clear');
        setFormData(initialFormState);
        setErrors({});
        setIsSubmitting(false);
      }
    };

    window.addEventListener('pageshow', handlePageShow);

    // Force clear on mount
    setTimeout(() => {
      console.log('Forced form clear after mount');
      setFormData(initialFormState);
      setErrors({});
      setIsSubmitting(false);
    }, 100);

    // Cleanup
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
      window.removeEventListener('load', handleLoad);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      window.removeEventListener('pageshow', handlePageShow);
    };
  }, []);

  // Function to reset form to initial state
  const resetForm = () => {
    console.log('Manual reset triggered');
    setFormData(initialFormState);
    setErrors({});
    setIsSubmitting(false);
  };

  // Debug function to force clear form
  const debugClearForm = () => {
    console.log('Debug clear form triggered');
    console.log('Current formData:', formData);
    setFormData(initialFormState);
    setErrors({});
    setIsSubmitting(false);
    console.log('Form cleared, new formData:', initialFormState);
  };

  // Test function to check current form state
  const debugCheckForm = () => {
    console.log('=== FORM STATE DEBUG ===');
    console.log('Current formData:', formData);
    console.log('Initial form state:', initialFormState);
    console.log('Are they equal?', JSON.stringify(formData) === JSON.stringify(initialFormState));
    console.log('Current errors:', errors);
    console.log('Is submitting:', isSubmitting);
    console.log('========================');
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    
    // Handle numeric fields - only allow positive integers
    if (['tenure_months', 'open_positions', 'available_positions', 'experience_min', 'experience_max', 'budget_min', 'budget_max'].includes(name)) {
      const numValue = value.replace(/[^0-9]/g, '');
      setFormData(prev => ({ ...prev, [name]: numValue }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.jd_title.trim()) {
      newErrors.jd_title = 'JD Title is required';
    }
    
    if (!formData.primary_skill.trim()) {
      newErrors.primary_skill = 'Primary Skill is required';
    }
    
    if (!formData.mode) {
      newErrors.mode = 'Mode is required';
    }
    
    if (!formData.tenure_months) {
      newErrors.tenure_months = 'Tenure is required';
    }
    
    if (!formData.open_positions) {
      newErrors.open_positions = 'Open Positions is required';
    }
    
    // Validate numeric ranges
    if (formData.experience_min && formData.experience_max && 
        parseInt(formData.experience_min) > parseInt(formData.experience_max)) {
      newErrors.experience_max = 'Max experience must be greater than min experience';
    }
    
    if (formData.budget_min && formData.budget_max && 
        parseInt(formData.budget_min) > parseInt(formData.budget_max)) {
      newErrors.budget_max = 'Max budget must be greater than min budget';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      toast.error('Please fix the errors before submitting');
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const payload = {
        ...formData,
        tenure_months: parseInt(formData.tenure_months),
        open_positions: parseInt(formData.open_positions),
        available_positions: parseInt(formData.available_positions) || 0,
        experience_min: parseInt(formData.experience_min) || 0,
        experience_max: parseInt(formData.experience_max) || 0,
        budget_min: parseInt(formData.budget_min) || 0,
        budget_max: parseInt(formData.budget_max) || 0
      };
      
      const response = await axios.post('/api/jd', payload);
      
      if (response.status === 200 || response.status === 201) {
        toast.success('Job Description saved successfully!');
        // Reset form after successful submission
        resetForm();
      }
    } catch (error) {
      console.error('Error saving JD:', error);
      toast.error(error.response?.data?.message || 'Failed to save Job Description');
    } finally {
      setIsSubmitting(false);
    }
  };

  const showHelp = () => {
    toast('Help: Fill in all required fields marked with *. Numeric fields accept only positive integers.', {
      duration: 5000,
      icon: 'ℹ️',
    });
  };

  const FormField = ({ label, name, type = 'text', required = false, placeholder = '', multiline = false, options = null }) => (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      
      {multiline ? (
        <textarea
          name={name}
          value={formData[name]}
          onChange={handleInputChange}
          placeholder={placeholder}
          rows={4}
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="off"
          spellCheck="false"
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
            errors[name] ? 'border-red-500' : 'border-gray-300'
          }`}
        />
      ) : options ? (
        <select
          name={name}
          value={formData[name]}
          onChange={handleInputChange}
          autoComplete="off"
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
            errors[name] ? 'border-red-500' : 'border-gray-300'
          }`}
        >
          <option value="">Select {label}</option>
          {options.map(option => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
      ) : (
        <input
          type={type}
          name={name}
          value={formData[name]}
          onChange={handleInputChange}
          placeholder={placeholder}
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="off"
          spellCheck="false"
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent ${
            errors[name] ? 'border-red-500' : 'border-gray-300'
          }`}
        />
      )}
      
      {errors[name] && (
        <p className="mt-1 text-sm text-red-600">{errors[name]}</p>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Job Description Entry</h1>
              <p className="mt-2 text-sm text-gray-600">
                Enter the job description details and click SAVE to proceed.
              </p>
            </div>
            <button
              onClick={showHelp}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              title="Help"
            >
              <QuestionMarkCircleIcon className="h-6 w-6" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <form onSubmit={handleSubmit} autoComplete="off">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            {/* Left Column - JD Details Form */}
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                  <InformationCircleIcon className="h-5 w-5 text-primary-500 mr-2" />
                  JD Details Form
                </h2>
                
                {/* Basic Information Section */}
                <div className="mb-6">
                  <h3 className="text-lg font-medium text-gray-800 mb-4">Basic Information</h3>
                  <FormField 
                    label="JD Title" 
                    name="jd_title" 
                    required 
                    placeholder="e.g., Senior React Developer"
                  />
                  <FormField 
                    label="Primary Skill" 
                    name="primary_skill" 
                    required 
                    placeholder="e.g., ReactJS"
                  />
                  <FormField 
                    label="Secondary Skills" 
                    name="secondary_skills" 
                    multiline 
                    placeholder="e.g., NodeJS, MySQL, TypeScript"
                  />
                  <FormField 
                    label="Mode" 
                    name="mode" 
                    required 
                    options={['Onsite', 'Remote', 'Hybrid']}
                  />
                  <FormField 
                    label="Tenure in months" 
                    name="tenure_months" 
                    type="number" 
                    required 
                    placeholder="12"
                  />
                  <FormField 
                    label="Open Positions" 
                    name="open_positions" 
                    type="number" 
                    required 
                    placeholder="5"
                  />
                  <FormField 
                    label="Available Positions" 
                    name="available_positions" 
                    type="number" 
                    placeholder="3"
                  />
                </div>
                
                {/* Fitment Criteria Section */}
                <div>
                  <h3 className="text-lg font-medium text-gray-800 mb-4">Fitment Criteria</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <FormField 
                      label="Op Experience Min" 
                      name="experience_min" 
                      type="number" 
                      placeholder="3"
                    />
                    <FormField 
                      label="Op Experience Max" 
                      name="experience_max" 
                      type="number" 
                      placeholder="5"
                    />
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <FormField 
                      label="Op Budget Min" 
                      name="budget_min" 
                      type="number" 
                      placeholder="60000"
                    />
                    <FormField 
                      label="Op Budget Max" 
                      name="budget_max" 
                      type="number" 
                      placeholder="90000"
                    />
                  </div>
                  <FormField 
                    label="JD Keywords" 
                    name="jd_keywords" 
                    multiline 
                    placeholder="e.g., React, JavaScript, Frontend, UI/UX"
                  />
                </div>
              </div>
            </div>
            
            {/* Right Column - From Customer */}
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                  <InformationCircleIcon className="h-5 w-5 text-primary-500 mr-2" />
                  From Customer
                </h2>
                
                {/* Original JD Section */}
                <div className="mb-6">
                  <h3 className="text-lg font-medium text-gray-800 mb-4">Original JD</h3>
                  <FormField 
                    label="JD Keywords" 
                    name="original_jd" 
                    multiline 
                    placeholder="Paste the full job description text here..."
                  />
                </div>
                
                {/* Notes Section */}
                <div>
                  <h3 className="text-lg font-medium text-gray-800 mb-4">Notes</h3>
                  <FormField 
                    label="Special Instruction" 
                    name="special_instruction" 
                    multiline 
                    placeholder="Any special instructions or requirements..."
                  />
                </div>
              </div>
            </div>
          </div>
          
          {/* Footer Action Area */}
          <div className="mt-8 flex justify-end space-x-4">
            <button
              type="button"
              onClick={resetForm}
              disabled={isSubmitting}
              className="px-6 py-3 bg-gray-500 text-white font-medium rounded-lg shadow-sm hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
            >
              Reset
            </button>
            <button
              type="button"
              onClick={debugClearForm}
              className="px-6 py-3 bg-blue-500 text-white font-medium rounded-lg shadow-sm hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
            >
              Debug Clear Form
            </button>
            <button
              type="button"
              onClick={debugCheckForm}
              className="px-6 py-3 bg-green-500 text-white font-medium rounded-lg shadow-sm hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors"
            >
              Debug Check Form
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className={`px-8 py-3 bg-primary-600 text-white font-medium rounded-lg shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors ${
                isSubmitting ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {isSubmitting ? 'Saving...' : 'SAVE'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default JobDescriptionEntry; 