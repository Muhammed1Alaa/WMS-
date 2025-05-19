import React, { useState, useEffect } from 'react';
import { StockMovement, MovementType } from '../types/movement';
import { movementsApi } from '../lib/api/movements';
import { itemsApi } from '../lib/api/items';
import { locationsApi } from '../lib/api/locations';
import { Item } from '../types/item';
import { StorageLocation } from '../types/location';

const Movements: React.FC = () => {
    const [movements, setMovements] = useState<StockMovement[]>([]);
    const [items, setItems] = useState<Item[]>([]);
    const [locations, setLocations] = useState<StorageLocation[]>([]);
    const [selectedItem, setSelectedItem] = useState<number | null>(null);
    const [quantity, setQuantity] = useState<number>(0);
    const [movementType, setMovementType] = useState<MovementType>('inbound');
    const [fromLocation, setFromLocation] = useState<number | null>(null);
    const [toLocation, setToLocation] = useState<number | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [movementsData, itemsData, locationsData] = await Promise.all([
                    movementsApi.getAll(),
                    itemsApi.getAll(),
                    locationsApi.getAll()
                ]);
                setMovements(movementsData);
                setItems(itemsData);
                setLocations(locationsData);
            } catch (err) {
                setError('Failed to fetch data');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedItem) return;

        try {
            const newMovement = await movementsApi.create({
                item_id: selectedItem,
                from_location_id: fromLocation || undefined,
                to_location_id: toLocation || undefined,
                quantity,
                movement_type: movementType
            });
            setMovements([newMovement, ...movements]);
            setQuantity(0);
            setFromLocation(null);
            setToLocation(null);
        } catch (err) {
            setError('Failed to create movement');
            console.error(err);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div className="text-red-500">{error}</div>;

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-2xl font-bold mb-6">Stock Movements</h1>
            
            <form onSubmit={handleSubmit} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Item
                    </label>
                    <select
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        value={selectedItem || ''}
                        onChange={(e) => setSelectedItem(Number(e.target.value))}
                        required
                    >
                        <option value="">Select an item</option>
                        {items.map((item) => (
                            <option key={item.id} value={item.id}>
                                {item.name} ({item.barcode})
                            </option>
                        ))}
                    </select>
                </div>

                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Movement Type
                    </label>
                    <select
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        value={movementType}
                        onChange={(e) => setMovementType(e.target.value as MovementType)}
                        required
                    >
                        <option value="inbound">Inbound</option>
                        <option value="outbound">Outbound</option>
                        <option value="move">Move</option>
                    </select>
                </div>

                {movementType === 'move' && (
                    <>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2">
                                From Location
                            </label>
                            <select
                                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                value={fromLocation || ''}
                                onChange={(e) => setFromLocation(Number(e.target.value))}
                                required
                            >
                                <option value="">Select a location</option>
                                {locations.map((location) => (
                                    <option key={location.id} value={location.id}>
                                        {location.name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2">
                                To Location
                            </label>
                            <select
                                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                value={toLocation || ''}
                                onChange={(e) => setToLocation(Number(e.target.value))}
                                required
                            >
                                <option value="">Select a location</option>
                                {locations.map((location) => (
                                    <option key={location.id} value={location.id}>
                                        {location.name}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </>
                )}

                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Quantity
                    </label>
                    <input
                        type="number"
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        value={quantity}
                        onChange={(e) => setQuantity(Number(e.target.value))}
                        min="0"
                        step="0.01"
                        required
                    />
                </div>

                <button
                    type="submit"
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >
                    Create Movement
                </button>
            </form>

            <div className="bg-white shadow-md rounded my-6">
                <table className="min-w-full">
                    <thead>
                        <tr className="bg-gray-100">
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Item
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Type
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Quantity
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                From
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                To
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Timestamp
                            </th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {movements.map((movement) => {
                            const item = items.find((i) => i.id === movement.item_id);
                            const fromLoc = locations.find((l) => l.id === movement.from_location_id);
                            const toLoc = locations.find((l) => l.id === movement.to_location_id);

                            return (
                                <tr key={movement.id}>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        {item?.name} ({item?.barcode})
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        {movement.movement_type}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        {movement.quantity}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        {fromLoc?.name || '-'}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        {toLoc?.name || '-'}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        {new Date(movement.timestamp).toLocaleString()}
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Movements; 