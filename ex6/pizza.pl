% Pizza Base Prices
pizza_config(veg, 150).
pizza_config(cheese, 200).
pizza_config(chicken, 250).

% Size Multipliers
size_multiplier(small, 1).
size_multiplier(medium, 1.5).
size_multiplier(large, 2).

% Dynamic Price Calculation
get_final_price(Type, Size, FinalPrice) :-
    pizza_config(Type, Base),
    size_multiplier(Size, Mult),
    FinalPrice is Base * Mult.

order :-
    take_order(0).

take_order(CurrentTotal) :-
    write('Enter pizza (veg/cheese/chicken): '), read(Type),
    write('Enter size (small/medium/large): '), read(Size),
    write('Enter quantity: '), read(Qty),

    (get_final_price(Type, Size, UnitPrice) ->
        Sub is UnitPrice * Qty,
        NewTotal is CurrentTotal + Sub,
        format('Item: ~w (~w), Qty: ~w, Subtotal: ~w~n', [Type, Size, Qty, Sub]),

        write('Order more? (yes/no): '), read(Choice),
        (Choice == yes -> take_order(NewTotal) ; format('Final Bill: ~w~n', [NewTotal]))
    ;
        write('Invalid choice! Try again.'), nl, take_order(CurrentTotal)
    ).
