import { useState, useEffect } from 'react';
import Head from 'next/head';
import { useAuth } from '../../services/auth';
import { todoAPI } from '../../services/api';
import TodoList from '../../components/todos/TodoList';

export default function Dashboard() {
  const { isAuthenticated: isAuth, currentUser: user, logout: signOut } = useAuth();
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState({ title: '', description: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Load todos when the component mounts
  useEffect(() => {
    if (isAuth) {
      loadTodos();
    }
  }, [isAuth]);

  // Ensure JWT token is set when user authenticates
  useEffect(() => {
    // The JWT token should already be set by the auth service
    // after successful authentication with BetterAuth
  }, [user]);

  const loadTodos = async () => {
    try {
      setLoading(true);
      const response = await todoAPI.getAll(user.id);
      setTodos(response.data.tasks);
    } catch (err) {
      setError('Failed to load todos: ' + (err.message || 'Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (e) => {
    e.preventDefault();

    if (!newTodo.title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      const response = await todoAPI.create(user.id, newTodo);
      setTodos([response.data.task, ...todos]);
      setNewTodo({ title: '', description: '' });
      setError('');
    } catch (err) {
      setError('Failed to add todo: ' + (err.message || 'Unknown error'));
    }
  };

  const handleToggleComplete = async (id) => {
    try {
      const response = await todoAPI.toggleComplete(user.id, id);
      setTodos(todos.map(todo =>
        todo.id === id ? response.data.task : todo
      ));
    } catch (err) {
      setError('Failed to update todo: ' + (err.message || 'Unknown error'));
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      await todoAPI.delete(user.id, id);
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (err) {
      setError('Failed to delete todo: ' + (err.message || 'Unknown error'));
    }
  };

  if (!isAuth) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center max-w-md mx-auto px-4">
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Welcome Back!</h1>
            <p className="text-gray-600 mb-6">Please sign in to access your todo dashboard</p>
            <div className="animate-pulse">
              <div className="w-24 h-8 bg-indigo-200 rounded mx-auto"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Head>
        <title>Dashboard - Todo Web Application</title>
      </Head>

      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-xl font-semibold text-gray-900 flex items-center">
                  <svg className="w-6 h-6 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  Todo Dashboard
                </h1>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600 hidden sm:block">Welcome, {user?.email}</span>
              <button
                onClick={() => signOut()}
                className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-full shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {error && (
          <div className="mb-6 rounded-lg bg-red-50 border border-red-200 p-4 animate-pulse">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white shadow-lg rounded-2xl p-6 mb-8 border border-gray-100 transition-all duration-300 hover:shadow-xl">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <svg className="w-6 h-6 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Add New Todo
          </h2>
          <form onSubmit={handleAddTodo} className="space-y-4">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                Task Title *
              </label>
              <input
                type="text"
                id="title"
                value={newTodo.title}
                onChange={(e) => setNewTodo({...newTodo, title: e.target.value})}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200 text-base"
                placeholder="What needs to be done today?"
                maxLength={255}
              />
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                id="description"
                value={newTodo.description}
                onChange={(e) => setNewTodo({...newTodo, description: e.target.value})}
                rows="3"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200 resize-none text-base"
                placeholder="Add more details about this task..."
                maxLength={1000}
              />
            </div>
            <div>
              <button
                type="submit"
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-xl shadow-sm text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transform transition-all duration-200 hover:scale-105"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Add Todo
              </button>
            </div>
          </form>
        </div>

        <div className="bg-white shadow-lg rounded-2xl p-6 border border-gray-100 transition-all duration-300">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-800 flex items-center">
              <svg className="w-6 h-6 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Your Tasks
              <span className="ml-2 bg-indigo-100 text-indigo-800 text-sm font-medium px-2.5 py-0.5 rounded-full">
                {todos.length}
              </span>
            </h2>
            {todos.length > 0 && (
              <div className="text-sm text-gray-500">
                {todos.filter(todo => !todo.is_completed).length} pending, {todos.filter(todo => todo.is_completed).length} completed
              </div>
            )}
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="flex flex-col items-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
                <p className="text-gray-600">Loading your tasks...</p>
              </div>
            </div>
          ) : (
            <TodoList
              todos={todos}
              onToggle={handleToggleComplete}
              onDelete={handleDeleteTodo}
              onEdit={async (id, updatedData) => {
                try {
                  const response = await todoAPI.update(user.id, id, updatedData);
                  setTodos(todos.map(todo =>
                    todo.id === id ? response.data.task : todo
                  ));
                } catch (err) {
                  setError('Failed to update todo: ' + (err.message || 'Unknown error'));
                }
              }}
            />
          )}
        </div>
      </main>
    </div>
  );
}