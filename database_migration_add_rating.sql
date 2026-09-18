alter table partners
add column if not exists rating decimal(3, 1);

update partners
set rating = case inn
    when '7701234567' then 4.8
    when '5001098765' then 4.2
    when '7812345678' then 10.0
    else rating
end;
