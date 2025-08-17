import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { PlusIcon, PencilIcon, TrashIcon, EyeIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import jdService from '../services/jdService';
import SectionHeader from '../components/SectionHeader';

const JDReport = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedJob, setSelectedJob] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showHelp, setShowHelp] = useState(false);

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = async () => {
    try {
      setLoading(true);
      const response = await jdService.getAllJobs();
      setJobs(response.data || []);
    } catch (error) {
      toast.error('Failed to load job descriptions');
      console.error('Error loading jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (jobId) => {
    if (window.confirm('Are you sure you want to delete this job description?')) {
      try {
        await jdService.deleteJob(jobId);
        toast.success('Job description deleted successfully');
        loadJobs();
      } catch (error) {
        toast.error('Failed to delete job description');
      }
    }
  };

  const handleView = (job) => {
    setSelectedJob(job);
    setShowModal(true);
  };

  const handleHelpClick = () => {
    setShowHelp(true);
  };

  const closeHelp = () => {
    setShowHelp(false);
  };

  const formatSkills = (skills) => {
    if (!skills) return 'N/A';
    try {
      const skillsArray = typeof skills === 'string' ? JSON.parse(skills) : skills;
      return Array.isArray(skillsArray) ? skillsArray.join(', ') : 'N/A';
    } catch {
      return skills || 'N/A';
    }
  };

  const formatKeywords = (keywords) => {
    if (!keywords) return 'N/A';
    try {
      const keywordsArray = typeof keywords === 'string' ? JSON.parse(keywords) : keywords;
      return Array.isArray(keywordsArray) ? keywordsArray.join(', ') : 'N/A';
    } catch {
      return keywords || 'N/A';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Open': return 'bg-green-100 text-green-800';
      case 'In Progress': return 'bg-blue-100 text-blue-800';
      case 'On Hold': return 'bg-yellow-100 text-yellow-800';
      case 'Closed': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getModeColor = (mode) => {
    switch (mode) {
      case 'Remote': return 'bg-purple-100 text-purple-800';
      case 'Onsite': return 'bg-indigo-100 text-indigo-800';
      case 'Hybrid': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading job descriptions...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <SectionHeader 
          title="Job Description Report"
          subtitle={`Showing ${jobs.length} job descriptions`}
        />

        {/* Action Bar */}
        <div className="mb-6 flex justify-between items-center">
          <div className="flex space-x-4">
            <button
              onClick={() => loadJobs()}
              className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
            >
              Refresh
            </button>
            <button
              onClick={() => jdService.updateAging()}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Update Aging
            </button>
            <button
              onClick={handleHelpClick}
              className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 flex items-center"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.564-.227 1.24-.227 1.808 0 .564.227 1.24.227 1.808 0 .564-.227 1.24-.227 1.808 0 .564.227 1.24.227 1.808 0M9 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Help
            </button>
          </div>
                     <Link
             to="/"
             className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
           >
            <PlusIcon className="h-5 w-5 mr-2" />
            Add New Job
          </Link>
        </div>

        {/* Jobs Table */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Job Details
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Customer & Skills
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Requirements
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status & Aging
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {jobs.map((job) => (
                  <tr key={job.jd_id} className="hover:bg-gray-50">
                    {/* Job Details Column */}
                    <td className="px-6 py-4">
                      <div className="space-y-2">
                        <div>
                          <h3 className="text-sm font-medium text-gray-900">
                            {job.jd_title}
                          </h3>
                          <p className="text-xs text-gray-500">
                            ID: {job.jd_id}
                          </p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getModeColor(job.job_mode_name)}`}>
                            {job.job_mode_name}
                          </span>
                          <span className="text-xs text-gray-500">
                            {job.jd_tenure} months
                          </span>
                        </div>
                        <p className="text-xs text-gray-600 line-clamp-2">
                          {job.jd_original?.substring(0, 100)}...
                        </p>
                      </div>
                    </td>

                    {/* Customer & Skills Column */}
                    <td className="px-6 py-4">
                      <div className="space-y-2">
                        <div>
                          <p className="text-sm font-medium text-gray-900">
                            {job.customer_name}
                          </p>
                          <p className="text-xs text-gray-500">
                            {job.jd_consumer}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-600">
                            <span className="font-medium">Category:</span> {job.skillset_category_name || 'N/A'}
                          </p>
                          <p className="text-xs text-gray-600">
                            <span className="font-medium">Skills:</span> {formatSkills(job.jd_skillset)}
                          </p>
                        </div>
                      </div>
                    </td>

                    {/* Requirements Column */}
                    <td className="px-6 py-4">
                      <div className="space-y-2">
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="font-medium">Exp:</span> {job.jd_op_exp_min}-{job.jd_op_exp_max} yrs
                          </div>
                          <div>
                            <span className="font-medium">Budget:</span> ${job.jd_op_budget_min?.toLocaleString()}-${job.jd_op_budget_max?.toLocaleString()}
                          </div>
                        </div>
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="font-medium">Positions:</span> {job.jd_open_position || 'N/A'}
                          </div>
                          <div>
                            <span className="font-medium">Revenue:</span> {job.jd_revenue_potential || 'N/A'}
                          </div>
                        </div>
                        <p className="text-xs text-gray-600">
                          <span className="font-medium">Keywords:</span> {formatKeywords(job.jd_keywords)}
                        </p>
                      </div>
                    </td>

                    {/* Status & Aging Column */}
                    <td className="px-6 py-4">
                      <div className="space-y-2">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(job.job_status_name)}`}>
                          {job.job_status_name}
                        </span>
                        <div className="text-xs text-gray-600">
                          <p><span className="font-medium">Created:</span> {new Date(job.jd_created_date).toLocaleDateString()}</p>
                          <p><span className="font-medium">Aging:</span> {job.jd_aging || 0} days</p>
                          <p><span className="font-medium">By:</span> {job.created_by_name}</p>
                        </div>
                      </div>
                    </td>

                    {/* Actions Column */}
                    <td className="px-6 py-4">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleView(job)}
                          className="text-blue-600 hover:text-blue-900"
                          title="View Details"
                        >
                          <EyeIcon className="h-5 w-5" />
                        </button>
                        <button
                          onClick={() => {/* TODO: Implement edit */}}
                          className="text-green-600 hover:text-green-900"
                          title="Edit"
                        >
                          <PencilIcon className="h-5 w-5" />
                        </button>
                        <button
                          onClick={() => handleDelete(job.jd_id)}
                          className="text-red-600 hover:text-red-900"
                          title="Delete"
                        >
                          <TrashIcon className="h-5 w-5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {jobs.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500">No job descriptions found.</p>
              <Link
                to="/"
                className="mt-4 inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                Create Your First Job Description
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Job Details Modal */}
      {showModal && selectedJob && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-900">
                  Job Description Details
                </h3>
                <button
                  onClick={() => setShowModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ×
                </button>
              </div>
              
              <div className="space-y-4 max-h-96 overflow-y-auto">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Title:</label>
                    <p className="text-sm text-gray-900">{selectedJob.jd_title}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700">Customer:</label>
                    <p className="text-sm text-gray-900">{selectedJob.customer_name}</p>
                  </div>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-700">Description:</label>
                  <p className="text-sm text-gray-900 mt-1">{selectedJob.jd_original}</p>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Skills:</label>
                    <p className="text-sm text-gray-900">{formatSkills(selectedJob.jd_skillset)}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700">Keywords:</label>
                    <p className="text-sm text-gray-900">{formatKeywords(selectedJob.jd_keywords)}</p>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Experience:</label>
                    <p className="text-sm text-gray-900">{selectedJob.jd_op_exp_min}-{selectedJob.jd_op_exp_max} years</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700">Budget:</label>
                    <p className="text-sm text-gray-900">
                      {selectedJob.jd_currency === 'INR' ? '₹' : '$'}
                      {selectedJob.jd_op_budget_min?.toLocaleString()}-{selectedJob.jd_op_budget_max?.toLocaleString()}
                    </p>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Mode:</label>
                    <p className="text-sm text-gray-900">{selectedJob.job_mode_name}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700">Status:</label>
                    <p className="text-sm text-gray-900">{selectedJob.job_status_name}</p>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Created:</label>
                    <p className="text-sm text-gray-900">{new Date(selectedJob.jd_created_date).toLocaleDateString()}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700">Aging:</label>
                    <p className="text-sm text-gray-900">{selectedJob.jd_aging || 0} days</p>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 flex justify-end">
                <button
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
      
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
                  <li>• View and manage all job descriptions</li>
                  <li>• Track job status and aging</li>
                  <li>• Generate comprehensive reports</li>
                  <li>• Export data for analysis</li>
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
  );
};

export default JDReport; 