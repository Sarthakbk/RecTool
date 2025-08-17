import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import jdService from '../services/jdService';
import FormField from '../components/FormField';

const JDEntry = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [scanning, setScanning] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [categories, setCategories] = useState([]);
  const [statuses, setStatuses] = useState([]);
  const [users, setUsers] = useState([]);
  const [currencies, setCurrencies] = useState([]);
  
  // Default users for Created By dropdown
  const defaultUsers = [
    { user_id: 1, full_name: 'Nikitha' },
    { user_id: 2, full_name: 'Gauthami' }
  ];
  
  const [formData, setFormData] = useState({
    jd_title: '',
    jd_customer_id: '1', // Default to sample customer ID
    jd_consumer: '',
    jd_original: '', // Ensure this is initialized as empty string
    jd_skillset_cat: '1', // Default to sample category ID
    jd_skillset: [],
    jd_mode: '',
    jd_tenure: '',
    jd_op_exp_min: '',
    jd_op_exp_max: '',
    jd_op_budget_min: '',
    jd_op_budget_max: '',
    jd_open_position: '',
    jd_available_pos: '',
    jd_revenue_potential: '',
    jd_currency: 'USD',  // Default to USD
    jd_keywords: [],
    jd_source: '',
    jd_special_instruction: '',
    jd_created_by: '',
    jd_status: '1' // Default to active status
  });

  const [skillInput, setSkillInput] = useState('');
  const [keywordInput, setKeywordInput] = useState('');
  
  // Mode options with descriptions
  const modeOptions = [
    { value: 1, label: 'Remote', description: 'Work from anywhere' },
    { value: 2, label: 'Onsite', description: 'Work at office location' },
    { value: 3, label: 'Hybrid', description: 'Combination of remote and onsite work' },
    { value: 4, label: 'Contract', description: 'Contract-based work arrangement' },
    { value: 5, label: 'Part-time', description: 'Part-time work arrangement' }
  ];

  useEffect(() => {
    loadReferenceData();
  }, []);

  const loadReferenceData = async () => {
    try {
      const [categoriesRes, statusesRes, usersRes, currenciesRes] = await Promise.all([
        jdService.getCategories(),
        jdService.getStatuses(),
        jdService.getUsers(),
        jdService.getCurrencies()
      ]);

      setCategories(categoriesRes.data || []);
      setStatuses(statusesRes.data || []);
      setUsers(usersRes.data || []);
      setCurrencies(currenciesRes.data || []);
    } catch (error) {
      toast.error('Failed to load reference data');
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const addSkill = () => {
    if (skillInput.trim() && !formData.jd_skillset.includes(skillInput.trim())) {
      setFormData(prev => ({
        ...prev,
        jd_skillset: [...prev.jd_skillset, skillInput.trim()]
      }));
      setSkillInput('');
    }
  };

  const removeSkill = (skillToRemove) => {
    setFormData(prev => ({
      ...prev,
      jd_skillset: prev.jd_skillset.filter(skill => skill !== skillToRemove)
    }));
  };

  const addKeyword = () => {
    if (keywordInput.trim() && !formData.jd_keywords.includes(keywordInput.trim())) {
      setFormData(prev => ({
        ...prev,
        jd_keywords: [...prev.jd_keywords, keywordInput.trim()]
      }));
      setKeywordInput('');
    }
  };

  const removeKeyword = (keywordToRemove) => {
    setFormData(prev => ({
      ...prev,
      jd_keywords: prev.jd_keywords.filter(keyword => keyword !== keywordToRemove)
    }));
  };

  // Function to scan and extract JD information
  const handleScanJD = async () => {
    if (!formData.jd_original || typeof formData.jd_original !== 'string' || !formData.jd_original.trim()) {
      toast.error('Please enter job description text first');
      return;
    }

    setScanning(true);
    try {
      const response = await jdService.scanJobDescription(formData.jd_original);
      if (response.success && response.data) {
        setFormData(prev => ({
          ...prev,
          ...response.data
        }));
        toast.success('Job description scanned successfully!');
      } else {
        toast.error('Failed to scan job description. Please try again.');
      }
    } catch (error) {
      toast.error('Failed to scan job description. Please try again.');
    } finally {
      setScanning(false);
    }
  };

  const handleHelpClick = () => {
    setShowHelp(true);
  };

  const closeHelp = () => {
    setShowHelp(false);
  };

  // Function to reset form to initial state
  const resetForm = () => {
    setFormData({
      jd_title: '',
      jd_customer_id: '1', // Default to sample customer ID
      jd_consumer: '',
      jd_original: '', // Ensure this is initialized as empty string
      jd_skillset_cat: '1', // Default to sample category ID
      jd_skillset: [],
      jd_mode: '',
      jd_tenure: '',
      jd_op_exp_min: '',
      jd_op_exp_max: '',
      jd_op_budget_min: '',
      jd_op_budget_max: '',
      jd_open_position: '',
      jd_available_pos: '',
      jd_revenue_potential: '',
      jd_currency: 'USD',  // Default to USD
      jd_keywords: [],
      jd_source: '',
      jd_special_instruction: '',
      jd_created_by: '',
      jd_status: '1' // Default to active status
    });
    setSkillInput('');
    setKeywordInput('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate required fields
    const requiredFields = [
      'jd_title', 'jd_customer_id', 'jd_consumer', 'jd_original', 
      'jd_mode', 'jd_tenure', 'jd_op_exp_min', 'jd_op_exp_max',
      'jd_op_budget_min', 'jd_op_budget_max', 'jd_created_by'
    ];
    
    const missingFields = requiredFields.filter(field => {
      const value = formData[field];
      return value === '' || value === null || value === undefined;
    });
    
    if (missingFields.length > 0) {
      const fieldNames = missingFields.map(field => {
        const name = field.replace('jd_', '');
        return name.charAt(0).toUpperCase() + name.slice(1);
      });
      toast.error(`Please fill in required fields: ${fieldNames.join(', ')}`);
      return;
    }
    
    if (!formData.jd_skillset.length) {
      toast.error('Please add at least one skill');
      return;
    }

    setLoading(true);
    try {
      // Convert arrays to JSON strings for backend
      const submitData = {
        ...formData,
        jd_skillset: JSON.stringify(formData.jd_skillset),
        jd_keywords: formData.jd_keywords.length > 0 ? JSON.stringify(formData.jd_keywords) : null,
        jd_customer_id: parseInt(formData.jd_customer_id),
        jd_tenure: parseInt(formData.jd_tenure),
        jd_op_exp_min: parseFloat(formData.jd_op_exp_min),
        jd_op_exp_max: parseFloat(formData.jd_op_exp_max),
        jd_op_budget_min: parseFloat(formData.jd_op_budget_min),
        jd_op_budget_max: parseFloat(formData.jd_op_budget_max),
        jd_open_position: formData.jd_open_position ? parseInt(formData.jd_open_position) : null,
        jd_mode: parseInt(formData.jd_mode),
        jd_created_by: parseInt(formData.jd_created_by),
        jd_status: parseInt(formData.jd_status)
      };
      
      const response = await jdService.createJob(submitData);
      toast.success('Job Description created successfully!');
      resetForm(); // Reset form to blank state
    } catch (error) {
      if (error.response) {
        toast.error(error.response.data?.error || 'Failed to create job description');
      } else if (error.request) {
        toast.error('No response from server. Please check your connection.');
      } else {
        toast.error('An error occurred while creating job description');
      }
    } finally {
      setLoading(false);
    }
  };

  // Combine API users with default users, avoiding duplicates
  const allUsers = [
    ...defaultUsers,
    ...(users.filter(user => !defaultUsers.find(du => du.user_id === user.user_id)))
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Job Description Entry</h1>
            <p className="mt-2 text-gray-600">Enter the job description details and click SAVE to proceed.</p>
          </div>
          <div className="flex items-center gap-3">
            <button
              type="button"
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              title="Help"
              onClick={handleHelpClick}
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.564-.227 1.24-.227 1.808 0 .564.227 1.24.227 1.808 0 .564-.227 1.24-.227 1.808 0 .564.227 1.24.227 1.808 0M9 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </button>
          </div>
        </div>

        {/* Main Content Area - Two Columns */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            {/* Left Column - JD Details Form */}
            <div className="space-y-6">
              
              {/* Basic Information Section */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h2 className="text-lg font-bold text-gray-900 mb-4">Basic Information</h2>
                <div className="space-y-4">
                  <FormField
                    label="JD Title"
                    value={formData.jd_title}
                    onChange={(value) => handleInputChange('jd_title', value)}
                    required
                    placeholder="Enter job title"
                  />
                  
                  <FormField
                    label="Customer"
                    type="select"
                    value={formData.jd_customer_id}
                    onChange={(value) => handleInputChange('jd_customer_id', value)}
                    required
                    placeholder="Select customer"
                    options={[
                      { value: '1', label: 'Sample Company' }
                    ]}
                  />
                  
                  <FormField
                    label="Company"
                    value={formData.jd_consumer}
                    onChange={(value) => handleInputChange('jd_consumer', value)}
                    required
                    placeholder="Enter company name"
                  />
                  
                  <FormField
                    label="Primary Skill"
                    value={formData.jd_skillset.length > 0 ? formData.jd_skillset[0] : ''}
                    onChange={(value) => {
                      if (formData.jd_skillset.length > 0) {
                        const newSkills = [...formData.jd_skillset];
                        newSkills[0] = value;
                        handleInputChange('jd_skillset', newSkills);
                      } else {
                        handleInputChange('jd_skillset', [value]);
                      }
                    }}
                    required
                    placeholder="Enter primary skill"
                  />
                  
                  <div className="space-y-2">
                    <label className="block text-sm font-medium text-gray-700">
                      Secondary Skills
                    </label>
                    <textarea
                      value={formData.jd_skillset.slice(1).join(', ')}
                      onChange={(e) => {
                        const primarySkill = formData.jd_skillset[0] || '';
                        const secondarySkills = e.target.value.split(',').map(s => s.trim()).filter(s => s);
                        handleInputChange('jd_skillset', [primarySkill, ...secondarySkills].filter(s => s));
                      }}
                      placeholder="Enter secondary skills (comma-separated)"
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  
                  <FormField
                    label="Mode"
                    type="select"
                    value={formData.jd_mode}
                    onChange={(value) => handleInputChange('jd_mode', value)}
                    required
                    placeholder="Select work mode"
                    options={modeOptions}
                  />
                  
                  <FormField
                    label="Tenure in months"
                    type="number"
                    value={formData.jd_tenure}
                    onChange={(value) => handleInputChange('jd_tenure', value)}
                    required
                    placeholder="Enter tenure"
                    step="1"
                  />
                  
                  <div className="grid grid-cols-2 gap-4">
                    <FormField
                      label="Open Positions"
                      type="number"
                      value={formData.jd_open_position}
                      onChange={(value) => handleInputChange('jd_open_position', value)}
                      placeholder="Number of positions"
                      step="1"
                    />
                    
                    <FormField
                      label="Available Positions"
                      value={formData.jd_available_pos}
                      onChange={(value) => handleInputChange('jd_available_pos', value)}
                      placeholder="Available positions"
                    />
                  </div>
                  
                  <FormField
                    label="Created By"
                    type="select"
                    value={formData.jd_created_by}
                    onChange={(value) => handleInputChange('jd_created_by', value)}
                    required
                    placeholder="Select user"
                    options={allUsers.map(user => ({ value: user.user_id, label: user.full_name }))}
                  />
                  
                  <FormField
                    label="Job Status"
                    type="select"
                    value={formData.jd_status}
                    onChange={(value) => handleInputChange('jd_status', value)}
                    required
                    placeholder="Select status"
                    options={[
                      { value: '1', label: 'Active' },
                      { value: '2', label: 'Draft' },
                      { value: '3', label: 'Closed' }
                    ]}
                  />
                </div>
              </div>
              
              {/* Fitment Criteria Section */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h2 className="text-lg font-bold text-gray-900 mb-4">Fitment Criteria</h2>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <FormField
                      label="Op Experience Min"
                      type="number"
                      value={formData.jd_op_exp_min}
                      onChange={(value) => handleInputChange('jd_op_exp_min', value)}
                      required
                      placeholder="Min years"
                      step="0.5"
                    />
                    
                    <FormField
                      label="Op Experience Max"
                      type="number"
                      value={formData.jd_op_exp_max}
                      onChange={(value) => handleInputChange('jd_op_exp_max', value)}
                      required
                      placeholder="Max years"
                      step="0.5"
                    />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <FormField
                      label="Op Budget Min"
                      type="number"
                      value={formData.jd_op_budget_min}
                      onChange={(value) => handleInputChange('jd_op_budget_min', value)}
                      required
                      placeholder="Enter minimum budget"
                      step="1000"
                    />
                    
                    <FormField
                      label="Op Budget Max"
                      type="number"
                      value={formData.jd_op_budget_max}
                      onChange={(value) => handleInputChange('jd_op_budget_max', value)}
                      required
                      placeholder="Enter maximum budget"
                      step="1000"
                    />
                  </div>
                  
                  <FormField
                    label="Currency"
                    type="select"
                    value={formData.jd_currency}
                    onChange={(value) => handleInputChange('jd_currency', value)}
                    required
                    placeholder="Select currency"
                    options={currencies.map(currency => ({ 
                      value: currency.currency_code, 
                      label: `${currency.currency_name} (${currency.symbol})` 
                    }))}
                  />
                  
                  <div className="space-y-2">
                    <label className="block text-sm font-medium text-gray-700">
                      JD Keywords
                    </label>
                    <textarea
                      value={formData.jd_keywords.join(', ')}
                      onChange={(e) => {
                        const keywords = e.target.value.split(',').map(k => k.trim()).filter(k => k);
                        handleInputChange('jd_keywords', keywords);
                      }}
                      placeholder="Enter keywords (comma-separated)"
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>
              </div>
            </div>
            
            {/* Right Column - From Customer */}
            <div className="space-y-6">
              
              {/* Original JD Section */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h2 className="text-lg font-bold text-gray-900 mb-4">Original JD</h2>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <label className="block text-sm font-medium text-gray-700">
                      JD Keywords
                    </label>
                    <textarea
                      value={formData.jd_original}
                      onChange={(e) => handleInputChange('jd_original', e.target.value)}
                      required
                      placeholder="Paste the original job description here..."
                      rows={12}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  
                  <div className="flex justify-center">
                    <button
                      type="button"
                      onClick={handleScanJD}
                      disabled={scanning || !formData.jd_original || typeof formData.jd_original !== 'string' || !formData.jd_original.trim()}
                      className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      {scanning ? 'Scanning...' : 'SCAN & EXTRACT'}
                    </button>
                  </div>
                </div>
              </div>
              
              {/* Notes Section */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h2 className="text-lg font-bold text-gray-900 mb-4">Notes</h2>
                <div className="space-y-4">
                  <FormField
                    label="Source"
                    value={formData.jd_source}
                    onChange={(value) => handleInputChange('jd_source', value)}
                    placeholder="Job source (e.g., LinkedIn, Indeed)"
                  />
                  
                  <div className="space-y-2">
                    <label className="block text-sm font-medium text-gray-700">
                      Special Instruction
                    </label>
                    <textarea
                      value={formData.jd_special_instruction}
                      onChange={(value) => handleInputChange('jd_special_instruction', value)}
                      placeholder="Enter special instructions or notes..."
                      rows={4}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Footer Action Area */}
          <div className="flex justify-end pt-6">
            <button
              type="submit"
              disabled={loading}
              className="px-8 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Saving...' : 'SAVE'}
            </button>
          </div>
        </form>
        
        {/* Help Modal */}
        {showHelp && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold text-gray-900">Need Help?</h3>
                <button
                  onClick={closeHelp}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <div className="space-y-4">
                <p className="text-gray-600">
                  We're here to help you with the Job Description Management System.
                </p>
                
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-semibold text-blue-900 mb-2">Contact Support</h4>
                  <div className="space-y-2">
                    <div className="flex items-center">
                      <svg className="w-5 h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                      </svg>
                      <a 
                        href="https://www.ankyahnexus.com" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 font-medium underline"
                      >
                        www.ankyahnexus.com
                      </a>
                    </div>
                    <p className="text-sm text-blue-700">
                      Visit our website for support and more information
                    </p>
                  </div>
                </div>
                
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-900 mb-2">System Features</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Scan and extract job description information automatically</li>
                    <li>• Manage job descriptions with comprehensive details</li>
                    <li>• Track skills, experience, and budget requirements</li>
                    <li>• Generate reports and analytics</li>
                  </ul>
                </div>
                
                <div className="text-center pt-4">
                  <button
                    onClick={closeHelp}
                    className="px-6 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors"
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default JDEntry; 