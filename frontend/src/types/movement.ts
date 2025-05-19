export type MovementType = 'inbound' | 'outbound' | 'move';

export interface StockMovement {
    id: number;
    item_id: number;
    user_id: number;
    from_location_id?: number;
    to_location_id?: number;
    quantity: number;
    movement_type: MovementType;
    timestamp: string;
}

export interface CreateStockMovement {
    item_id: number;
    from_location_id?: number;
    to_location_id?: number;
    quantity: number;
    movement_type: MovementType;
} 