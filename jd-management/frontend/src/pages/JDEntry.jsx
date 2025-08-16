import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import jdService from '../services/jdService';
import FormField from '../components/FormField';
import SectionHeader from '../components/SectionHeader';

const JDEntry = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [categories, setCategories] = useState([]);
  const [modes, setModes] = useState([]);
  const [statuses, setStatuses] = useState([]);
  const [users, setUsers] = useState([]);
  const [customers, setCustomers] = useState([]);
  
  const [formData, setFormData] = useState({
    jd_title: 'Test Job Title',
    jd_customer_id: 1,
    jd_consumer: 'Test Company',
    jd_original: 'This is a test job description for debugging purposes.',
    jd_skillset_cat: '',
    jd_skillset: ['JavaScript', 'React'],
    jd_mode: 1,
    jd_tenure: 12,
    jd_op_exp_min: 3.0,
    jd_op_exp_max: 5.0,
    jd_op_budget_min: 60000,
    jd_op_budget_max: 90000,
    jd_open_position: 2,
    jd_available_pos: 'Available',
    jd_revenue_potential: 'High',
    jd_keywords: ['Frontend', 'Development'],
    jd_source: 'Test Source',
    jd_special_instruction: 'Test instructions',
    jd_created_by: 1,
    jd_status: 1
  });

  // Default users for Created By dropdown
  const defaultUsers = [
    { user_id: 1, full_name: 'Nikitha' },
    { user_id: 2, full_name: 'Gauthami' }
  ];

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
      const [categoriesRes, modesRes, statusesRes, usersRes] = await Promise.all([
        jdService.getCategories(),
        jdService.getModes(),
        jdService.getStatuses(),
        jdService.getUsers()
      ]);

      setCategories(categoriesRes.data || []);
      setModes(modesRes.data || []);
      setStatuses(statusesRes.data || []);
      setUsers(usersRes.data || []);

      // Set default values for demo
      setFormData(prev => ({ 
        ...prev, 
        jd_created_by: 1, // Default to Nikitha
        jd_customer_id: 1, // Default to first customer
        jd_status: 1 // Default to first status
      }));
    } catch (error) {
      toast.error('Failed to load reference data');
    }
  };

  const handleInputChange = (field, value) => {
    console.log(`Updating ${field}:`, value);
    setFormData(prev => {
      const newData = { ...prev, [field]: value };
      console.log('Updated form data:', newData);
      return newData;
    });
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    console.log('Form data before validation:', formData);
    
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
      console.log('Missing fields:', missingFields);
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
      
      console.log('Submitting data:', submitData);
      
      const response = await jdService.createJob(submitData);
      console.log('Response:', response);
      toast.success('Job Description created successfully!');
      navigate('/jd-report');
    } catch (error) {
      console.error('Submit error:', error);
      if (error.response) {
        console.error('Error response:', error.response);
        console.error('Error data:', error.response.data);
        toast.error(error.response.data?.error || 'Failed to create job description');
      } else if (error.request) {
        console.error('Error request:', error.request);
        toast.error('No response from server. Please check your connection.');
      } else {
        console.error('Error message:', error.message);
        toast.error(`Error: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-4 sm:py-6 lg:py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <SectionHeader 
          title="Create New Job Description"
          subtitle="Fill in the details below to create a new job posting"
        />

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-4 sm:p-6 lg:p-8 space-y-4 sm:space-y-6">
          {/* Quick Mode Selection */}
          <div className="bg-gray-50 p-4 sm:p-6 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Quick Mode Selection</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2 sm:gap-3">
              {modeOptions.map((mode) => (
                <button
                  key={mode.value}
                  type="button"
                  onClick={() => handleInputChange('jd_mode', mode.value)}
                  className={`px-3 py-2 text-sm rounded-md border transition-colors ${
                    formData.jd_mode == mode.value
                      ? 'bg-blue-600 text-white border-blue-600'
                      : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  {mode.label}
                </button>
              ))}
            </div>
          </div>
          
          {/* Basic Information */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <FormField
              label="Job Title *"
              type="text"
              value={formData.jd_title}
              onChange={(value) => handleInputChange('jd_title', value)}
              required
              placeholder="e.g., Senior React Developer"
            />
            
            <FormField
              label="Customer ID *"
              type="number"
              value={formData.jd_customer_id}
              onChange={(value) => handleInputChange('jd_customer_id', value)}
              required
              placeholder="1"
            />
            
            <FormField
              label="Consumer *"
              type="text"
              value={formData.jd_consumer}
              onChange={(value) => handleInputChange('jd_consumer', value)}
              required
              placeholder="e.g., TechCorp Solutions"
            />
          </div>

          {/* Required Fields Notice */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
            <p className="text-sm text-blue-800">
              <span className="font-medium">Note:</span> Fields marked with * are required. 
              Make sure to fill in all required fields before submitting.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <FormField
              label="Skillset Category"
              type="select"
              value={formData.jd_skillset_cat}
              onChange={(value) => handleInputChange('jd_skillset_cat', value)}
              options={categories.map(cat => ({ value: cat.category_id, label: cat.category_name }))}
              placeholder="Select category"
            />
            
            <FormField
              label="Tenure (months) *"
              type="number"
              value={formData.jd_tenure}
              onChange={(value) => handleInputChange('jd_tenure', value)}
              required
              placeholder="12"
            />
            
            <FormField
              label="Revenue Potential"
              type="text"
              value={formData.jd_revenue_potential}
              onChange={(value) => handleInputChange('jd_revenue_potential', value)}
              placeholder="e.g., High, Medium, Low"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <FormField
              label="Status"
              type="select"
              value={formData.jd_status}
              onChange={(value) => handleInputChange('jd_status', value)}
              options={statuses.map(status => ({ value: status.status_id, label: status.status_name }))}
              placeholder="Select status"
            />
            
            <div>
              <FormField
                label="Created By *"
                type="select"
                value={formData.jd_created_by}
                onChange={(value) => handleInputChange('jd_created_by', value)}
                required
                options={[
                  ...defaultUsers,
                  ...users.filter(user => !defaultUsers.find(du => du.user_id === user.user_id))
                ].map(user => ({ value: user.user_id, label: user.full_name }))}
                placeholder="Select user"
              />
              {formData.jd_created_by && (
                <div className="mt-2">
                  <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                    <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                    Created by: {defaultUsers.find(u => u.user_id == formData.jd_created_by)?.full_name || 
                                 users.find(u => u.user_id == formData.jd_created_by)?.full_name}
                  </div>
                </div>
              )}
            </div>
            
            <div></div> {/* Empty div for grid alignment */}
          </div>

          {/* Job Description */}
          <div className="col-span-full">
            <FormField
              label="Original Job Description *"
              type="textarea"
              value={formData.jd_original}
              onChange={(value) => handleInputChange('jd_original', value)}
              required
              placeholder="Paste the original job description here..."
              rows={4}
            />
          </div>

                    {/* Skills and Keywords */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Skillset * (Add at least one skill)
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={skillInput}
                  onChange={(e) => setSkillInput(e.target.value)}
                  placeholder="e.g., React, JavaScript"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill())}
                />
                <button
                  type="button"
                  onClick={addSkill}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Add
                </button>
              </div>
              {formData.jd_skillset.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {formData.jd_skillset.map((skill, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800"
                    >
                      {skill}
                      <button
                        type="button"
                        onClick={() => removeSkill(skill)}
                        className="ml-2 text-blue-600 hover:text-blue-800"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Keywords
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={keywordInput}
                  onChange={(e) => setKeywordInput(e.target.value)}
                  placeholder="e.g., Frontend, Web Development"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addKeyword())}
                />
                <button
                  type="button"
                  onClick={addKeyword}
                  className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
                >
                  Add
                </button>
              </div>
              {formData.jd_keywords.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {formData.jd_keywords.map((keyword, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-3 py-2 rounded-full text-sm bg-gray-100 text-gray-800"
                    >
                      {keyword}
                      <button
                        type="button"
                        onClick={() => removeKeyword(keyword)}
                        className="ml-2 text-gray-600 hover:text-gray-800"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Job Details */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <div>
              <FormField
                label="Job Mode *"
                type="select"
                value={formData.jd_mode}
                onChange={(value) => handleInputChange('jd_mode', value)}
                required
                options={modeOptions}
                placeholder="Select mode"
              />
              {formData.jd_mode && (
                <div className="mt-2">
                  <p className="text-sm text-gray-600 mb-2">
                    {modeOptions.find(mode => mode.value == formData.jd_mode)?.description}
                  </p>
                  <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                    <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                    {modeOptions.find(mode => mode.value == formData.jd_mode)?.label}
                  </div>
                </div>
              )}
            </div>
            
            <FormField
              label="Open Positions"
              type="number"
              value={formData.jd_open_position}
              onChange={(value) => handleInputChange('jd_open_position', value)}
              placeholder="3"
            />
            
            <FormField
              label="Available Positions"
              type="text"
              value={formData.jd_available_pos}
              onChange={(value) => handleInputChange('jd_available_pos', value)}
              placeholder="e.g., 2 available"
            />
          </div>

          {/* Experience Requirements */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            <FormField
              label="Min Experience (years) *"
              type="number"
              step="0.5"
              value={formData.jd_op_exp_min}
              onChange={(value) => handleInputChange('jd_op_exp_min', value)}
              required
              placeholder="3.0"
            />
            
            <FormField
              label="Max Experience (years) *"
              type="number"
              step="0.5"
              value={formData.jd_op_exp_max}
              onChange={(value) => handleInputChange('jd_op_exp_max', value)}
              required
              placeholder="5.0"
            />
            
            <FormField
              label="Min Budget ($) *"
              type="number"
              value={formData.jd_op_budget_min}
              onChange={(value) => handleInputChange('jd_op_budget_min', value)}
              required
              placeholder="60000"
            />
            
            <FormField
              label="Max Budget ($) *"
              type="number"
              value={formData.jd_op_budget_max}
              onChange={(value) => handleInputChange('jd_op_budget_max', value)}
              required
              placeholder="90000"
            />
          </div>

          {/* Additional Details */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <FormField
              label="Source"
              type="text"
              value={formData.jd_source}
              onChange={(value) => handleInputChange('jd_source', value)}
              placeholder="e.g., Company Website, Job Board"
            />
            
            <div className="sm:col-span-2 lg:col-span-1">
              <FormField
                label="Special Instructions"
                type="textarea"
                value={formData.jd_special_instruction}
                onChange={(value) => handleInputChange('jd_special_instruction', value)}
                placeholder="Any special requirements or instructions..."
                rows={3}
              />
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex flex-col sm:flex-row justify-end gap-4 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={() => {
                console.log('Current form data:', formData);
                console.log('Form validation check...');
                const requiredFields = [
                  'jd_title', 'jd_customer_id', 'jd_consumer', 'jd_original', 
                  'jd_mode', 'jd_tenure', 'jd_op_exp_min', 'jd_op_exp_max',
                  'jd_op_budget_min', 'jd_op_budget_max', 'jd_created_by'
                ];
                const missingFields = requiredFields.filter(field => {
                  const value = formData[field];
                  return value === '' || value === null || value === undefined;
                });
                console.log('Missing fields:', missingFields);
                console.log('Skills count:', formData.jd_skillset.length);
              }}
              className="px-4 py-2 border border-yellow-300 text-yellow-700 rounded-md hover:bg-yellow-50"
            >
              Debug Form
            </button>
            <button
              type="button"
              onClick={() => navigate('/jd-report')}
              className="px-6 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Creating...' : 'Create Job Description'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default JDEntry; 