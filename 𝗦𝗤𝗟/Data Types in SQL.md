# <span style="color:#4CAF50;">SQL Data Types - Short Notes</span>

<table>
<tr>
<th style="background-color:#1E88E5;color:white;">Data Type</th>
<th style="background-color:#1E88E5;color:white;">Description</th>
<th style="background-color:#1E88E5;color:white;">Example</th>
</tr>

<tr><td><code>SMALLINT</code></td><td>Stores small whole numbers.</td><td><code>25</code></td></tr>
<tr><td><code>INT</code> / <code>INTEGER</code></td><td>Stores whole numbers.</td><td><code>100</code></td></tr>
<tr><td><code>BIGINT</code></td><td>Stores very large whole numbers.</td><td><code>9876543210</code></td></tr>
<tr><td><code>SERIAL</code></td><td>Auto-incrementing integer (commonly used for IDs).</td><td><code>1, 2, 3...</code></td></tr>
<tr><td><code>BIGSERIAL</code></td><td>Auto-incrementing BIGINT.</td><td><code>1, 2, 3...</code></td></tr>
<tr><td><code>CHAR(n)</code></td><td>Stores fixed-length text.</td><td><code>CHAR(5)</code></td></tr>
<tr><td><code>VARCHAR(n)</code></td><td>Stores variable-length text (max <code>n</code> characters).</td><td><code>VARCHAR(50)</code></td></tr>
<tr><td><code>TEXT</code></td><td>Stores long text with no practical length limit.</td><td><code>"This is a long description..."</code></td></tr>
<tr><td><code>DECIMAL(p,s)</code></td><td>Stores exact decimal numbers.</td><td><code>999.99</code></td></tr>
<tr><td><code>NUMERIC(p,s)</code></td><td>Same as <code>DECIMAL</code>; exact decimal values.</td><td><code>1250.50</code></td></tr>
<tr><td><code>REAL</code></td><td>Stores single-precision decimal numbers.</td><td><code>3.14</code></td></tr>
<tr><td><code>DOUBLE PRECISION</code></td><td>Stores double-precision decimal numbers.</td><td><code>3.1415926535</code></td></tr>
<tr><td><code>BOOLEAN</code></td><td>Stores logical values (<code>TRUE</code> or <code>FALSE</code>).</td><td><code>TRUE</code></td></tr>
<tr><td><code>DATE</code></td><td>Stores date only.</td><td><code>2026-07-02</code></td></tr>
<tr><td><code>TIME</code></td><td>Stores time only.</td><td><code>14:30:45</code></td></tr>
<tr><td><code>TIMESTAMP</code></td><td>Stores both date and time.</td><td><code>2026-07-02 14:30:45</code></td></tr>
<tr><td><code>UUID</code></td><td>Stores universally unique identifiers.</td><td><code>550e8400-e29b...</code></td></tr>
<tr><td><code>JSON</code></td><td>Stores JSON data.</td><td><code>{"name":"Harsh"}</code></td></tr>
<tr><td><code>JSONB</code></td><td>Binary JSON (faster and more efficient than JSON).</td><td><code>{"age":23}</code></td></tr>
<tr><td><code>BYTEA</code></td><td>Stores binary data (images, files, etc.).</td><td>Binary data</td></tr>

</table>

## <span style="color:#FF9800;">⭐ Most Important Data Types for Beginners</span>

<table>
<tr>
<th style="background-color:#43A047;color:white;">Data Type</th>
<th style="background-color:#43A047;color:white;">Purpose</th>
</tr>

<tr><td><code>SERIAL</code></td><td>Auto-generated IDs</td></tr>
<tr><td><code>INT</code></td><td>Whole numbers</td></tr>
<tr><td><code>VARCHAR(n)</code></td><td>Short text</td></tr>
<tr><td><code>TEXT</code></td><td>Long text</td></tr>
<tr><td><code>DECIMAL(10,2)</code></td><td>Money / Prices</td></tr>
<tr><td><code>BOOLEAN</code></td><td>True / False</td></tr>
<tr><td><code>DATE</code></td><td>Date</td></tr>
<tr><td><code>TIME</code></td><td>Time</td></tr>
<tr><td><code>TIMESTAMP</code></td><td>Date & Time</td></tr>

</table>

These are the data types you'll use in **90% of SQL projects**.