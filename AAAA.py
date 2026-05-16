import plotly.express as px
import pandas as pd
import numpy as np

# 1. SAMPLE DATA (Replace this with your actual 'bookings' DataFrame)
np.random.seed(42)
dates = pd.date_range(start='2026-05-01', end='2026-05-31', freq='h')
bookings = pd.DataFrame({
    'book_date': np.random.choice(dates, size=1500),
    'total_amount': np.random.uniform(1000, 15000, size=1500)
})

# 2. GROUP BY DAY AND SUM TOTAL AMOUNT
# Convert to datetime, normalize to date (day), group, and sum
bookings['book_date'] = pd.to_datetime(bookings['book_date'])
bookings['day'] = bookings['book_date'].dt.date
daily_revenue = bookings.groupby('day')['total_amount'].sum().reset_index()

# 3. CREATE INTERACTIVE LINE CHART
fig = px.line(
    daily_revenue,
    x='day',
    y='total_amount',
    markers=True,
    title='Daily Booking Revenue Over Time',
    labels={
        'day': 'Date',
        'total_amount': 'Total Revenue ($)'
    },
    template='plotly_white'
)

# 4. CUSTOMIZE LINE AND MARKER COLOR
# 'line_color' sets the path color; 'color_discrete_sequence' overrides defaults
fig.update_traces(
    line_color='#e74c3c',  # Custom stylish red color line
    marker=dict(size=8, color='#2c3e50')  # Dark contrast color for dots
)

fig.update_layout(
    title_font_size=16,
    xaxis_tickformat='%b %d, %Y',  # Formats dates as 'May 01, 2026'
)

# Render interactive chart
fig.show()
