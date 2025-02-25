create table house_mkt_data
(
    id                    integer primary key autoincrement,
    statistics_date       date     not null,
    date_time             datetime not null,
    subscription_sets     int      not null,
    deals_sets            int      not null,
    city_projects_oneline int      not null,
    city_area_online      double   not null,
    yearly_listed_area    double   not null,
    yearly_deals_area     double   not null,
    monthly_listed_area   double   not null,
    monthly_deals_area    double   not null,
    raw_text              text     not null
);