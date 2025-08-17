import React from 'react';

const FormField = ({ 
  label, 
  type = 'text', 
  value, 
  onChange, 
  required = false, 
  placeholder = '', 
  error = '', 
  options = [],
  rows = 3,
  step,
  icon: Icon,
  ...props 
}) => {
  const handleChange = (e) => {
    if (onChange) {
      onChange(e.target.value);
    }
  };

  const renderField = () => {
    switch (type) {
      case 'textarea':
        return (
          <textarea
            value={value || ''}
            onChange={handleChange}
            placeholder={placeholder}
            rows={rows}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
              error ? 'border-red-500' : 'border-gray-300'
            }`}
            {...props}
          />
        );
      
      case 'select':
        return (
          <select
            value={value || ''}
            onChange={handleChange}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
              error ? 'border-red-500' : 'border-gray-300'
            }`}
            {...props}
          >
            <option value="">{placeholder}</option>
            {options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        );
      
      case 'number':
        return (
          <input
            type="number"
            value={value || ''}
            onChange={handleChange}
            placeholder={placeholder}
            step={step}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
              error ? 'border-red-500' : 'border-gray-300'
            }`}
            {...props}
          />
        );
      
      default:
        return (
          <input
            type={type}
            value={value || ''}
            onChange={handleChange}
            placeholder={placeholder}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${
              error ? 'border-red-500' : 'border-gray-300'
            }`}
            {...props}
          />
        );
    }
  };

  return (
    <div className="space-y-2">
      <label className="flex items-center text-sm font-medium text-gray-700">
        {Icon && <Icon className="w-4 h-4 mr-2 text-gray-500" />}
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      {renderField()}
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

export default FormField; 