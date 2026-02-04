import { useState } from 'react';

export default function TodoItem({ todo, onToggle, onDelete, onEdit }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({
    title: todo.title,
    description: todo.description || '',
    is_completed: todo.is_completed
  });

  const handleEditChange = (e) => {
    const { name, value, type, checked } = e.target;
    setEditData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSaveEdit = () => {
    onEdit(todo.id, editData);
    setIsEditing(false);
  };

  const handleCancelEdit = () => {
    setEditData({
      title: todo.title,
      description: todo.description || '',
      is_completed: todo.is_completed
    });
    setIsEditing(false);
  };

  return (
    <div className={`bg-white border-l-4 rounded-xl shadow-sm mb-4 transition-all duration-200 hover:shadow-md ${
      todo.is_completed ? 'border-green-500 bg-green-50' : 'border-indigo-500 bg-white'
    }`}>
      {isEditing ? (
        <div className="p-5 space-y-4">
          <input
            type="text"
            name="title"
            value={editData.title}
            onChange={handleEditChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-base font-medium"
            placeholder="Task title..."
            autoFocus
          />
          <textarea
            name="description"
            value={editData.description}
            onChange={handleEditChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-base resize-none"
            rows="2"
            placeholder="Description..."
          />
          <div className="flex items-center justify-between pt-2">
            <div className="flex items-center">
              <input
                type="checkbox"
                name="is_completed"
                checked={editData.is_completed}
                onChange={handleEditChange}
                className="h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded mr-2"
              />
              <span className="text-sm text-gray-600">Mark as completed</span>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={handleCancelEdit}
                className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg text-sm font-medium hover:bg-gray-300 transition-colors duration-200"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveEdit}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors duration-200"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      ) : (
        <>
          <div className="p-5">
            <div className="flex justify-between items-start">
              <div className="flex items-start space-x-3 flex-1 min-w-0">
                <button
                  onClick={() => onToggle(todo.id)}
                  className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors duration-200 ${
                    todo.is_completed
                      ? 'bg-green-500 border-green-500 text-white'
                      : 'border-gray-300 hover:border-indigo-500'
                  }`}
                >
                  {todo.is_completed && (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  )}
                </button>
                <div className="flex-1 min-w-0">
                  <h3 className={`text-lg font-semibold ${
                    todo.is_completed
                      ? 'line-through text-gray-500 decoration-gray-400'
                      : 'text-gray-900'
                  }`}>
                    {todo.title}
                  </h3>
                  {todo.description && (
                    <p className={`text-base mt-2 ${
                      todo.is_completed
                        ? 'line-through text-gray-400 decoration-gray-300'
                        : 'text-gray-600'
                    }`}>
                      {todo.description}
                    </p>
                  )}
                  <div className="flex items-center justify-between mt-3 text-xs text-gray-500">
                    <div className="flex space-x-4">
                      <span className="flex items-center">
                        <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        {new Date(todo.created_at).toLocaleDateString()}
                      </span>
                      {todo.is_completed && (
                        <span className="flex items-center text-green-600">
                          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                          </svg>
                          Completed
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
              <div className="flex items-center space-x-2 ml-4 flex-shrink-0">
                <button
                  onClick={() => setIsEditing(true)}
                  className="p-2 text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors duration-200"
                  title="Edit task"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  onClick={() => onDelete(todo.id)}
                  className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors duration-200"
                  title="Delete task"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}