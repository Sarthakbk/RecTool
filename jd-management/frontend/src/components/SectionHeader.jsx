import React from 'react';
import { InformationCircleIcon } from '@heroicons/react/24/outline';

const SectionHeader = ({ title, icon = true, className = '' }) => {
  return (
    <h2 className={`text-xl font-semibold text-gray-900 mb-6 flex items-center ${className}`}>
      {icon && (
        <InformationCircleIcon className="h-5 w-5 text-primary-500 mr-2" />
      )}
      {title}
    </h2>
  );
};

export default SectionHeader; 