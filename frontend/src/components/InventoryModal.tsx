import { Fragment } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { useForm } from 'react-hook-form';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';

interface InventoryForm {
  name: string;
  sku: string;
  description: string;
  quantity: number;
  warehouse_id: number;
  location_id: number;
}

interface InventoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  item?: {
    id: number;
    name: string;
    sku: string;
    description: string;
    quantity: number;
    warehouse_id: number;
    location_id: number;
  };
}

export const InventoryModal = ({ isOpen, onClose, item }: InventoryModalProps) => {
  const queryClient = useQueryClient();
  const { register, handleSubmit, watch, formState: { errors } } = useForm<InventoryForm>({
    defaultValues: item,
  });

  const { data: warehouses } = useQuery({
    queryKey: ['warehouses'],
    queryFn: async () => {
      const response = await api.get('/warehouses');
      return response.data;
    },
  });

  const { data: locations } = useQuery({
    queryKey: ['locations', watch('warehouse_id')],
    queryFn: async () => {
      if (!watch('warehouse_id')) return [];
      const response = await api.get(`/warehouses/${watch('warehouse_id')}/locations`);
      return response.data;
    },
    enabled: !!watch('warehouse_id'),
  });

  const createMutation = useMutation({
    mutationFn: (data: InventoryForm) => api.post('/inventory', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['inventory'] });
      onClose();
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: InventoryForm) => api.put(`/inventory/${item?.id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['inventory'] });
      onClose();
    },
  });

  const onSubmit = (data: InventoryForm) => {
    if (item) {
      updateMutation.mutate(data);
    } else {
      createMutation.mutate(data);
    }
  };

  return (
    <Transition.Root show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
                <form onSubmit={handleSubmit(onSubmit)}>
                  <div>
                    <div className="mt-3 text-center sm:mt-5">
                      <Dialog.Title as="h3" className="text-base font-semibold leading-6 text-gray-900">
                        {item ? 'Edit Inventory Item' : 'Create Inventory Item'}
                      </Dialog.Title>
                      <div className="mt-6 space-y-6">
                        <div>
                          <label htmlFor="name" className="block text-sm font-medium leading-6 text-gray-900">
                            Name
                          </label>
                          <div className="mt-2">
                            <input
                              type="text"
                              {...register('name', { required: 'Name is required' })}
                              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            />
                            {errors.name && (
                              <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
                            )}
                          </div>
                        </div>

                        <div>
                          <label htmlFor="sku" className="block text-sm font-medium leading-6 text-gray-900">
                            SKU
                          </label>
                          <div className="mt-2">
                            <input
                              type="text"
                              {...register('sku', { required: 'SKU is required' })}
                              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            />
                            {errors.sku && (
                              <p className="mt-1 text-sm text-red-600">{errors.sku.message}</p>
                            )}
                          </div>
                        </div>

                        <div>
                          <label htmlFor="description" className="block text-sm font-medium leading-6 text-gray-900">
                            Description
                          </label>
                          <div className="mt-2">
                            <textarea
                              {...register('description')}
                              rows={3}
                              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            />
                          </div>
                        </div>

                        <div>
                          <label htmlFor="quantity" className="block text-sm font-medium leading-6 text-gray-900">
                            Quantity
                          </label>
                          <div className="mt-2">
                            <input
                              type="number"
                              {...register('quantity', {
                                required: 'Quantity is required',
                                min: { value: 0, message: 'Quantity must be greater than or equal to 0' },
                              })}
                              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            />
                            {errors.quantity && (
                              <p className="mt-1 text-sm text-red-600">{errors.quantity.message}</p>
                            )}
                          </div>
                        </div>

                        <div>
                          <label htmlFor="warehouse_id" className="block text-sm font-medium leading-6 text-gray-900">
                            Warehouse
                          </label>
                          <div className="mt-2">
                            <select
                              {...register('warehouse_id', { required: 'Warehouse is required' })}
                              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            >
                              <option value="">Select a warehouse</option>
                              {warehouses?.map((warehouse) => (
                                <option key={warehouse.id} value={warehouse.id}>
                                  {warehouse.name}
                                </option>
                              ))}
                            </select>
                            {errors.warehouse_id && (
                              <p className="mt-1 text-sm text-red-600">{errors.warehouse_id.message}</p>
                            )}
                          </div>
                        </div>

                        <div>
                          <label htmlFor="location_id" className="block text-sm font-medium leading-6 text-gray-900">
                            Location
                          </label>
                          <div className="mt-2">
                            <select
                              {...register('location_id', { required: 'Location is required' })}
                              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                              disabled={!watch('warehouse_id')}
                            >
                              <option value="">Select a location</option>
                              {locations?.map((location) => (
                                <option key={location.id} value={location.id}>
                                  {location.name}
                                </option>
                              ))}
                            </select>
                            {errors.location_id && (
                              <p className="mt-1 text-sm text-red-600">{errors.location_id.message}</p>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
                    <button
                      type="submit"
                      className="inline-flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 sm:col-start-2"
                    >
                      {item ? 'Update' : 'Create'}
                    </button>
                    <button
                      type="button"
                      className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:col-start-1 sm:mt-0"
                      onClick={onClose}
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
}; 