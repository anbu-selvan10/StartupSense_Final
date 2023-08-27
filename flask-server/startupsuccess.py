import numpy as np
import pandas as pd
import re
import pickle

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import preprocessing

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.tree import export_graphviz

df = pd.read_csv("F:\\StartupSense_Final\\StartupSenseModels\\investments_VC.csv", encoding='iso-8859-1')

df = df.rename(columns={' market ': "market", ' funding_total_usd ': "funding_total_usd"})

df['funding_total_usd']=df['funding_total_usd'].str.replace(',','')
df['funding_total_usd']=df['funding_total_usd'].str.replace(' ','')
df['funding_total_usd']=df['funding_total_usd'].str.replace('-','0') 
df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'])
df['founded_at'] =  pd.to_datetime(df['founded_at'], format='%Y-%m-%d', errors = 'coerce')
df['founded_at'] =  pd.to_datetime(df['founded_at'], format='%Y-%m-%d', errors = 'coerce')
df['first_funding_at'] =  pd.to_datetime(df['first_funding_at'], format='%Y-%m-%d', errors = 'coerce')
df['last_funding_at'] =  pd.to_datetime(df['last_funding_at'], format='%Y-%m-%d', errors = 'coerce') 
df['founded_year'] =  pd.to_datetime(df['founded_year'], format='%Y', errors = 'coerce')
df['founded_month'] =  pd.to_datetime(df['founded_month'], format='%Y-%m', errors = 'coerce')
df.market = df.market.str.strip() 

df['diff_funding_days'] = df["last_funding_at"] - df["first_funding_at"]

df['diff_funding_months'] = (df['last_funding_at'] - df['first_funding_at'])/np.timedelta64(1, 'M') 

df['total_investment'] = df['seed'] + df['venture'] + df['equity_crowdfunding'] + df['undisclosed'] + df['convertible_note'] + df['debt_financing'] + df['angel'] + df['grant'] + df['private_equity'] + df['post_ipo_equity'] + df['post_ipo_debt'] + df['secondary_market'] + df['product_crowdfunding']

df['diff_first_funding_months'] = (df['first_funding_at'] - df['founded_at'])/np.timedelta64(1, 'M')

df_for_pred = df.copy()
df_for_pred = df_for_pred.drop(columns=['homepage_url', 'category_list', 'state_code', 'founded_at', 'founded_month', 'founded_quarter', 'founded_year', 
                    'diff_first_funding_months', 'diff_funding_days', 'funding_total_usd', 'city', 'region', 'first_funding_at', 'last_funding_at'])
df_for_pred = df_for_pred.dropna(subset=['permalink', 'status', 'name', 'market', 'country_code', 'diff_funding_months']) 
df_for_pred.loc[:, 'diff_funding_year'] = round(df_for_pred['diff_funding_months']/12)

admin_services = str('Employer Benefits Programs, Human Resource Automation, Corporate IT, Distribution, Service Providers, Archiving Service, Call Center, Collection Agency, College Recruiting, Courier Service, Debt Collections, Delivery, Document Preparation, Employee Benefits, Extermination Service, Facilities Support Services, Housekeeping Service, Human Resources, Knowledge Management, Office Administration, Packaging Services, Physical Security, Project Management, Staffing Agency, Trade Shows, Virtual Workforce').split(', ')
advertising = str('Creative Industries, Promotional, Advertising Ad Exchange, Ad Network, Ad Retargeting, Ad Server, Ad Targeting, Advertising, Advertising Platforms, Affiliate Marketing, Local Advertising, Mobile Advertising, Outdoor Advertising, SEM, Social Media Advertising, Video Advertising').split(', ')
agriculture = str('Agriculture, AgTech, Animal Feed, Aquaculture, Equestrian, Farming, Forestry, Horticulture, Hydroponics, Livestock').split(', ')
app = str('Application Performance Monitoring, App Stores, Application Platforms, Enterprise Application, App Discovery, Apps, Consumer Applications, Enterprise Applications, Mobile Apps, Reading Apps, Web Apps').split(', ')
artificial_intelli = str('Artificial Intelligence, Intelligent Systems, Machine Learning, Natural Language Processing, Predictive Analytics').split(', ')
biotechnology = str('Synthetic Biology, Bio-Pharm, Bioinformatics, Biometrics, Biopharma, Biotechnology, Genetics, Life Science, Neuroscience, Quantified Self').split(', ')
clothing = str('Fashion, Laundry and Dry-cleaning, Lingerie, Shoes').split(', ')
shopping = str('Consumer Behavior, Customer Support Tools, Discounts, Reviews and Recommendations, Auctions, Classifieds, Collectibles, Consumer Reviews, Coupons, E-Commerce, E-Commerce Platforms, Flash Sale, Gift, Gift Card, Gift Exchange, Gift Registry, Group Buying, Local Shopping, Made to Order, Marketplace, Online Auctions, Personalization, Point of Sale, Price Comparison, Rental, Retail, Retail Technology, Shopping, Shopping Mall, Social Shopping, Sporting Goods, Vending and Concessions, Virtual Goods, Wholesale').split(', ')
community = str("Self Development, Sex, Forums, Match-Making, Babies, Identity, Women, Kids, Entrepreneur, Networking, Adult, Baby, Cannabis, Children, Communities, Dating, Elderly, Family, Funerals, Humanitarian, Leisure, LGBT, Lifestyle, Men's, Online Forums, Parenting, Pet, Private Social Networking, Professional Networking, Q&A, Religion, Retirement, Sex Industry, Sex Tech, Social, Social Entrepreneurship, Teenagers, Virtual World, Wedding, Women's, Young Adults").split(', ')
electronics  = str('Mac, iPod Touch, Tablets, iPad, iPhone, Computer, Consumer Electronics, Drones, Electronics, Google Glass, Mobile Devices, Nintendo, Playstation, Roku, Smart Home, Wearables, Windows Phone, Xbox').split(', ')
consumer_goods= str('Commodities, Sunglasses, Groceries, Batteries, Cars, Beauty, Comics, Consumer Goods, Cosmetics, DIY, Drones, Eyewear, Fast-Moving Consumer Goods, Flowers, Furniture, Green Consumer Goods, Handmade, Jewelry, Lingerie, Shoes, Tobacco, Toys').split(', ')
content = str('E-Books, MicroBlogging, Opinions, Blogging Platforms, Content Delivery Network, Content Discovery, Content Syndication, Creative Agency, DRM, EBooks, Journalism, News, Photo Editing, Photo Sharing, Photography, Printing, Publishing, Social Bookmarking, Video Editing, Video Streaming').split(', ')
data = str('Optimization, A/B Testing, Analytics, Application Performance Management, Artificial Intelligence, Big Data, Bioinformatics, Biometrics, Business Intelligence, Consumer Research, Data Integration, Data Mining, Data Visualization, Database, Facial Recognition, Geospatial, Image Recognition, Intelligent Systems, Location Based Services, Machine Learning, Market Research, Natural Language Processing, Predictive Analytics, Product Research, Quantified Self, Speech Recognition, Test and Measurement, Text Analytics, Usability Testing').split(', ')
design = str('Visualization, Graphics, Design, Designers, CAD, Consumer Research, Data Visualization, Fashion, Graphic Design, Human Computer Interaction, Industrial Design, Interior Design, Market Research, Mechanical Design, Product Design, Product Research, Usability Testing, UX Design, Web Design').split(', ')
education = str('Universities, College Campuses, University Students, High Schools, All Students, Colleges, Alumni, Charter Schools, College Recruiting, Continuing Education, Corporate Training, E-Learning, EdTech, Education, Edutainment, Higher Education, Language Learning, MOOC, Music Education, Personal Development, Primary Education, Secondary Education, Skill Assessment, STEM Education, Textbook, Training, Tutoring, Vocational Education').split(', ')
energy = str('Gas, Natural Gas Uses, Oil, Oil & Gas, Battery, Biofuel, Biomass Energy, Clean Energy, Electrical Distribution, Energy, Energy Efficiency, Energy Management, Energy Storage, Fossil Fuels, Fuel, Fuel Cell, Oil and Gas, Power Grid, Renewable Energy, Solar, Wind Energy').split(', ')
events = str('Concerts, Event Management, Event Promotion, Events, Nightclubs, Nightlife, Reservations, Ticketing, Wedding').split(', ')
financial = str('Debt Collecting, P2P Money Transfer, Investment Management, Trading, Accounting, Angel Investment, Asset Management, Auto Insurance, Banking, Bitcoin, Commercial Insurance, Commercial Lending, Consumer Lending, Credit, Credit Bureau, Credit Cards, Crowdfunding, Cryptocurrency, Debit Cards, Debt Collections, Finance, Financial Exchanges, Financial Services, FinTech, Fraud Detection, Funding Platform, Gift Card, Health Insurance, Hedge Funds, Impact Investing, Incubators, Insurance, InsurTech, Leasing, Lending, Life Insurance, Micro Lending, Mobile Payments, Payments, Personal Finance, Prediction Markets, Property Insurance, Real Estate Investment, Stock Exchanges, Trading Platform, Transaction Processing, Venture Capital, Virtual Currency, Wealth Management').split(', ')
food = str('Specialty Foods, Bakery, Brewing, Cannabis, Catering, Coffee, Confectionery, Cooking, Craft Beer, Dietary Supplements, Distillery, Farmers Market, Food and Beverage, Food Delivery, Food Processing, Food Trucks, Fruit, Grocery, Nutrition, Organic Food, Recipes, Restaurants, Seafood, Snack Food, Tea, Tobacco, Wine And Spirits, Winery').split(', ')
gaming = str('Game, Games, Casual Games, Console Games, Contests, Fantasy Sports, Gambling, Gamification, Gaming, MMO Games, Online Games, PC Games, Serious Games, Video Games').split(', ')
government = str('Polling, Governance, CivicTech, Government, GovTech, Law Enforcement, Military, National Security, Politics, Public Safety, Social Assistance').split(', ')
hardware= str('Cable, 3D, 3D Technology, Application Specific Integrated Circuit (ASIC), Augmented Reality, Cloud Infrastructure, Communication Hardware, Communications Infrastructure, Computer, Computer Vision, Consumer Electronics, Data Center, Data Center Automation, Data Storage, Drone Management, Drones, DSP, Electronic Design Automation (EDA), Electronics, Embedded Systems, Field-Programmable Gate Array (FPGA), Flash Storage, Google Glass, GPS, GPU, Hardware, Industrial Design, Laser, Lighting, Mechanical Design, Mobile Devices, Network Hardware, NFC, Nintendo, Optical Communication, Playstation, Private Cloud, Retail Technology, RFID, RISC, Robotics, Roku, Satellite Communication, Semiconductor, Sensor, Sex Tech, Telecommunications, Video Conferencing, Virtual Reality, Virtualization, Wearables, Windows Phone, Wireless, Xbox').split(', ')
health_care = str('Senior Health, Physicians, Electronic Health Records, Doctors, Healthcare Services, Diagnostics, Alternative Medicine, Assisted Living, Assistive Technology, Biopharma, Cannabis, Child Care, Clinical Trials, Cosmetic Surgery, Dental, Diabetes, Dietary Supplements, Elder Care, Electronic Health Record (EHR), Emergency Medicine, Employee Benefits, Fertility, First Aid, Funerals, Genetics, Health Care, Health Diagnostics, Home Health Care, Hospital, Medical, Medical Device, mHealth, Nursing and Residential Care, Nutraceutical, Nutrition, Outpatient Care, Personal Health, Pharmaceutical, Psychology, Rehabilitation, Therapeutics, Veterinary, Wellness').split(', ')
it = str('Distributors, Algorithms, ICT, M2M, Technology, Business Information Systems, CivicTech, Cloud Data Services, Cloud Management, Cloud Security, CMS, Contact Management, CRM, Cyber Security, Data Center, Data Center Automation, Data Integration, Data Mining, Data Visualization, Document Management, E-Signature, Email, GovTech, Identity Management, Information and Communications Technology (ICT), Information Services, Information Technology, Intrusion Detection, IT Infrastructure, IT Management, Management Information Systems, Messaging, Military, Network Security, Penetration Testing, Private Cloud, Reputation, Sales Automation, Scheduling, Social CRM, Spam Filtering, Technical Support, Unified Communications, Video Chat, Video Conferencing, Virtualization, VoIP').split(', ')
internet = str('Online Identity, Cyber, Portals, Web Presence Management, Domains, Tracking, Web Tools, Curated Web, Search, Cloud Computing, Cloud Data Services, Cloud Infrastructure, Cloud Management, Cloud Storage, Darknet, Domain Registrar, E-Commerce Platforms, Ediscovery, Email, Internet, Internet of Things, ISP, Location Based Services, Messaging, Music Streaming, Online Forums, Online Portals, Private Cloud, Product Search, Search Engine, SEM, Semantic Search, Semantic Web, SEO, SMS, Social Media, Social Media Management, Social Network, Unified Communications, Vertical Search, Video Chat, Video Conferencing, Visual Search, VoIP, Web Browsers, Web Hosting').split(', ')
invest = str('Angel Investment, Banking, Commercial Lending, Consumer Lending, Credit, Credit Cards, Financial Exchanges, Funding Platform, Hedge Funds, Impact Investing, Incubators, Micro Lending, Stock Exchanges, Trading Platform, Venture Capital').split(', ')
manufacturing = str('Innovation Engineering, Civil Engineers, Heavy Industry, Engineering Firms, Systems, 3D Printing, Advanced Materials, Foundries, Industrial, Industrial Automation, Industrial Engineering, Industrial Manufacturing, Machinery Manufacturing, Manufacturing, Paper Manufacturing, Plastics and Rubber Manufacturing, Textiles, Wood Processing').split(', ')
media = str('Writers, Creative, Television, Entertainment, Media, Advice, Animation, Art, Audio, Audiobooks, Blogging Platforms, Broadcasting, Celebrity, Concerts, Content, Content Creators, Content Discovery, Content Syndication, Creative Agency, Digital Entertainment, Digital Media, DRM, EBooks, Edutainment, Event Management, Event Promotion, Events, Film, Film Distribution, Film Production, Guides, In-Flight Entertainment, Independent Music, Internet Radio, Journalism, Media and Entertainment, Motion Capture, Music, Music Education, Music Label, Music Streaming, Music Venues, Musical Instruments, News, Nightclubs, Nightlife, Performing Arts, Photo Editing, Photo Sharing, Photography, Podcast, Printing, Publishing, Reservations, Social Media, Social News, Theatre, Ticketing, TV, TV Production, Video, Video Editing, Video on Demand, Video Streaming, Virtual World').split(', ')
message = str('Unifed Communications, Chat, Email, Meeting Software, Messaging, SMS, Unified Communications, Video Chat, Video Conferencing, VoIP, Wired Telecommunications').split(', ')
mobile = str('Android, Google Glass, iOS, mHealth, Mobile, Mobile Apps, Mobile Devices, Mobile Payments, Windows Phone, Wireless').split(', ')
music = str('Audio, Audiobooks, Independent Music, Internet Radio, Music, Music Education, Music Label, Music Streaming, Musical Instruments, Podcast').split(', ')
resource = str('Biofuel, Biomass Energy, Fossil Fuels, Mineral, Mining, Mining Technology, Natural Resources, Oil and Gas, Precious Metals, Solar, Timber, Water, Wind Energy').split(', ')
navigation = str('Maps, Geospatial, GPS, Indoor Positioning, Location Based Services, Mapping Services, Navigation').split(', ')
other = str('Mass Customization, Monetization, Testing, Subscription Businesses, Mobility, Incentives, Peer-to-Peer, Nonprofits, Alumni, Association, B2B, B2C, Blockchain, Charity, Collaboration, Collaborative Consumption, Commercial, Consumer, Crowdsourcing, Customer Service, Desktop Apps, Emerging Markets, Enterprise, Ethereum, Franchise, Freemium, Generation Y, Generation Z, Homeless Shelter, Infrastructure, Knowledge Management, LGBT Millennials, Non Profit, Peer to Peer, Professional Services, Project Management, Real Time, Retirement, Service Industry, Sharing Economy, Small and Medium Businesses, Social Bookmarking, Social Impact, Subscription Service, Technical Support, Underserved Children, Universities').split(', ')
payment = str('Billing, Bitcoin, Credit Cards, Cryptocurrency, Debit Cards, Fraud Detection, Mobile Payments, Payments, Transaction Processing, Virtual Currency').split(', ')
platforms = str('Development Platforms, Android, Facebook, Google, Google Glass, iOS, Linux, macOS, Nintendo, Operating Systems, Playstation, Roku, Tizen, Twitter, WebOS, Windows, Windows Phone, Xbox').split(', ')
privacy = str('Digital Rights Management, Personal Data, Cloud Security, Corrections Facilities, Cyber Security, DRM, E-Signature, Fraud Detection, Homeland Security, Identity Management, Intrusion Detection, Law Enforcement, Network Security, Penetration Testing, Physical Security, Privacy, Security').split(', ')
services = str('Funeral Industry, English-Speaking, Spas, Plumbers, Service Industries, Staffing Firms, Translation, Career Management, Business Services, Services, Accounting, Business Development, Career Planning, Compliance, Consulting, Customer Service, Employment, Environmental Consulting, Field Support, Freelance, Intellectual Property, Innovation Management, Legal, Legal Tech, Management Consulting, Outsourcing, Professional Networking, Quality Assurance, Recruiting, Risk Management, Social Recruiting, Translation Service').split(', ')
realestate= str('Office Space, Self Storage, Brokers, Storage, Home Owners, Self Storage , Realtors, Home & Garden, Utilities, Home Automation, Architecture, Building Maintenance, Building Material, Commercial Real Estate, Construction, Coworking, Facility Management, Fast-Moving Consumer Goods, Green Building, Home and Garden, Home Decor, Home Improvement, Home Renovation, Home Services, Interior Design, Janitorial Service, Landscaping, Property Development, Property Management, Real Estate, Real Estate Investment, Rental Property, Residential, Self-Storage, Smart Building, Smart Cities, Smart Home, Timeshare, Vacation Rental').split(', ')
sales = str('Advertising, Affiliate Marketing, App Discovery, App Marketing, Brand Marketing, Cause Marketing, Content Marketing, CRM, Digital Marketing, Digital Signage, Direct Marketing, Direct Sales, Email Marketing, Lead Generation, Lead Management, Local, Local Advertising, Local Business, Loyalty Programs, Marketing, Marketing Automation, Mobile Advertising, Multi-level Marketing, Outdoor Advertising, Personal Branding, Public Relations, Sales, Sales Automation, SEM, SEO, Social CRM, Social Media Advertising, Social Media Management, Social Media Marketing, Sponsorship, Video Advertising').split(', ')
science = str('Face Recognition, New Technologies, Advanced Materials, Aerospace, Artificial Intelligence, Bioinformatics, Biometrics, Biopharma, Biotechnology, Chemical, Chemical Engineering, Civil Engineering, Embedded Systems, Environmental Engineering, Human Computer Interaction, Industrial Automation, Industrial Engineering, Intelligent Systems, Laser, Life Science, Marine Technology, Mechanical Engineering, Nanotechnology, Neuroscience, Nuclear, Quantum Computing, Robotics, Semiconductor, Software Engineering, STEM Education').split(', ')
software = str('Business Productivity, 3D Technology, Android, App Discovery, Application Performance Management, Apps, Artificial Intelligence, Augmented Reality, Billing, Bitcoin, Browser Extensions, CAD, Cloud Computing, Cloud Management, CMS, Computer Vision, Consumer Applications, Consumer Software, Contact Management, CRM, Cryptocurrency, Data Center Automation, Data Integration, Data Storage, Data Visualization, Database, Developer APIs, Developer Platform, Developer Tools, Document Management, Drone Management, E-Learning, EdTech, Electronic Design Automation (EDA), Embedded Software, Embedded Systems, Enterprise Applications, Enterprise Resource Planning (ERP), Enterprise Software, Facial Recognition, File Sharing, IaaS, Image Recognition, iOS, Linux, Machine Learning, macOS, Marketing Automation, Meeting Software, Mobile Apps, Mobile Payments, MOOC, Natural Language Processing, Open Source, Operating Systems, PaaS, Predictive Analytics, Presentation Software, Presentations, Private Cloud, Productivity Tools, QR Codes, Reading Apps, Retail Technology, Robotics, SaaS, Sales Automation, Scheduling, Sex Tech, Simulation, SNS, Social CRM, Software, Software Engineering, Speech Recognition, Task Management, Text Analytics, Transaction Processing, Video Conferencing, Virtual Assistant, Virtual Currency, Virtual Desktop, Virtual Goods, Virtual Reality, Virtual World, Virtualization, Web Apps, Web Browsers, Web Development').split(', ')
sports = str('American Football, Baseball, Basketball, Boating, Cricket, Cycling, Diving, eSports, Fantasy Sports, Fitness, Golf, Hockey, Hunting, Outdoors, Racing, Recreation, Rugby, Sailing, Skiing, Soccer, Sporting Goods, Sports, Surfing, Swimming, Table Tennis, Tennis, Ultimate Frisbee, Volley Ball').split(', ')
sustainability = str('Green, Wind, Biomass Power Generation, Renewable Tech, Environmental Innovation, Renewable Energies, Clean Technology, Biofuel, Biomass Energy, Clean Energy, CleanTech, Energy Efficiency, Environmental Engineering, Green Building, Green Consumer Goods, GreenTech, Natural Resources, Organic, Pollution Control, Recycling, Renewable Energy, Solar, Sustainability, Waste Management, Water Purification, Wind Energy').split(', ')
transportation = str('Taxis, Air Transportation, Automotive, Autonomous Vehicles, Car Sharing, Courier Service, Delivery Service, Electric Vehicle, Ferry Service, Fleet Management, Food Delivery, Freight Service, Last Mile Transportation, Limousine Service, Logistics, Marine Transportation, Parking, Ports and Harbors, Procurement, Public Transportation, Railroad, Recreational Vehicles, Ride Sharing, Same Day Delivery, Shipping, Shipping Broker, Space Travel, Supply Chain Management, Taxi Service, Transportation, Warehousing, Water Transportation').split(', ')
travel = str('Adventure Travel, Amusement Park and Arcade, Business Travel, Casino, Hospitality, Hotel, Museums and Historical Sites, Parks, Resorts, Timeshare, Tour Operator, Tourism, Travel, Travel Accommodations, Travel Agency, Vacation Rental').split(', ')
video = str('Animation, Broadcasting, Film, Film Distribution, Film Production, Motion Capture, TV, TV Production, Video, Video Editing, Video on Demand, Video Streaming').split(', ')

df_for_pred['Industry Group'] = np.where(df_for_pred.market.str.contains('|'.join(admin_services), flags=re.IGNORECASE), "Administrative Services",
                               np.where(df_for_pred.market.str.contains('|'.join(software), flags=re.IGNORECASE), "Software", 
                               np.where(df_for_pred.market.str.contains('|'.join(advertising), flags=re.IGNORECASE), "Advertising",
                               np.where(df_for_pred.market.str.contains('|'.join(agriculture), flags=re.IGNORECASE), "Agriculture and Farming",
                               np.where(df_for_pred.market.str.contains('|'.join(app), flags=re.IGNORECASE), "Apps", 
                               np.where(df_for_pred.market.str.contains('|'.join(artificial_intelli), flags=re.IGNORECASE), "Artificial Intelligence", 
                               np.where(df_for_pred.market.str.contains('|'.join(biotechnology), flags=re.IGNORECASE), "Biotechnology", 
                               np.where(df_for_pred.market.str.contains('|'.join(clothing), flags=re.IGNORECASE), "Clothing and Apparel", 
                               np.where(df_for_pred.market.str.contains('|'.join(shopping), flags=re.IGNORECASE), "Commerce and Shopping", 
                               np.where(df_for_pred.market.str.contains('|'.join(community), flags=re.IGNORECASE), "Community and Lifestyle", 
                               np.where(df_for_pred.market.str.contains('|'.join(electronics), flags=re.IGNORECASE), "Consumer Electronics", 
                               np.where(df_for_pred.market.str.contains('|'.join(consumer_goods), flags=re.IGNORECASE), "Consumer Goods", 
                               np.where(df_for_pred.market.str.contains('|'.join(content), flags=re.IGNORECASE), "Content and Publishing", 
                               np.where(df_for_pred.market.str.contains('|'.join(data), flags=re.IGNORECASE), "Data and Analytics",
                               np.where(df_for_pred.market.str.contains('|'.join(design), flags=re.IGNORECASE), "Design", 
                               np.where(df_for_pred.market.str.contains('|'.join(education), flags=re.IGNORECASE), "Education", 
                               np.where(df_for_pred.market.str.contains('|'.join(energy), flags=re.IGNORECASE), "Energy", 
                               np.where(df_for_pred.market.str.contains('|'.join(events), flags=re.IGNORECASE), "Events", 
                               np.where(df_for_pred.market.str.contains('|'.join(financial), flags=re.IGNORECASE), "Financial Services",
                               np.where(df_for_pred.market.str.contains('|'.join(food), flags=re.IGNORECASE), "Food and Beverage", 
                               np.where(df_for_pred.market.str.contains('|'.join(gaming), flags=re.IGNORECASE), "Gaming", 
                               np.where(df_for_pred.market.str.contains('|'.join(government), flags=re.IGNORECASE), "Government and Military", 
                               np.where(df_for_pred.market.str.contains('|'.join(hardware), flags=re.IGNORECASE), "Hardware",
                               np.where(df_for_pred.market.str.contains('|'.join(health_care), flags=re.IGNORECASE), "Health Care",
                               np.where(df_for_pred.market.str.contains('|'.join(it), flags=re.IGNORECASE), "Information Technology", 
                               np.where(df_for_pred.market.str.contains('|'.join(internet), flags=re.IGNORECASE), "Internet Services", 
                               np.where(df_for_pred.market.str.contains('|'.join(invest), flags=re.IGNORECASE), "Lending and Investments", 
                               np.where(df_for_pred.market.str.contains('|'.join(manufacturing), flags=re.IGNORECASE), "Manufacturing",
                               np.where(df_for_pred.market.str.contains('|'.join(media), flags=re.IGNORECASE), "Media and Entertainment",
                               np.where(df_for_pred.market.str.contains('|'.join(message), flags=re.IGNORECASE), "Messaging and Telecommunication", 
                               np.where(df_for_pred.market.str.contains('|'.join(mobile), flags=re.IGNORECASE), "Mobile", 
                               np.where(df_for_pred.market.str.contains('|'.join(music), flags=re.IGNORECASE), "Music and Audio", 
                               np.where(df_for_pred.market.str.contains('|'.join(resource), flags=re.IGNORECASE), "Natural Resources",
                               np.where(df_for_pred.market.str.contains('|'.join(navigation), flags=re.IGNORECASE), "Navigation and Mapping",
                               np.where(df_for_pred.market.str.contains('|'.join(payment), flags=re.IGNORECASE), "Payments", 
                               np.where(df_for_pred.market.str.contains('|'.join(platforms), flags=re.IGNORECASE), "Platforms", 
                               np.where(df_for_pred.market.str.contains('|'.join(privacy), flags=re.IGNORECASE), "Privacy and Security", 
                               np.where(df_for_pred.market.str.contains('|'.join(services), flags=re.IGNORECASE), "Professional Services",
                               np.where(df_for_pred.market.str.contains('|'.join(realestate), flags=re.IGNORECASE), "Real Estate", 
                               np.where(df_for_pred.market.str.contains('|'.join(sales), flags=re.IGNORECASE), "Sales and Marketing", 
                               np.where(df_for_pred.market.str.contains('|'.join(science), flags=re.IGNORECASE), "Science and Engineering", 
                               np.where(df_for_pred.market.str.contains('|'.join(sports), flags=re.IGNORECASE), "Sports",
                               np.where(df_for_pred.market.str.contains('|'.join(sustainability), flags=re.IGNORECASE), "Sustainability", 
                               np.where(df_for_pred.market.str.contains('|'.join(transportation), flags=re.IGNORECASE), "Transportation", 
                               np.where(df_for_pred.market.str.contains('|'.join(travel), flags=re.IGNORECASE), "Travel and Tourism", 
                               np.where(df_for_pred.market.str.contains('|'.join(video), flags=re.IGNORECASE), "Video",
                               np.where(df_for_pred.market.str.contains('|'.join(other), flags=re.IGNORECASE), "Other",  "Other")))))))))))))))))))))))))))))))))))))))))))))))

df_for_pred.groupby('Industry Group')['permalink'].count().sort_values(ascending = False)

df_for_pred_final = df_for_pred.copy()
df_for_pred_final = df_for_pred_final.drop(columns=['diff_funding_months', 'market'], axis=1)
df_for_pred_final[['funding_rounds', 'seed', 'venture', 'equity_crowdfunding',
       'undisclosed', 'convertible_note', 'debt_financing', 'angel', 'grant',
       'private_equity', 'post_ipo_equity', 'post_ipo_debt',
       'secondary_market', 'product_crowdfunding', 'round_A', 'round_B',
       'round_C', 'round_D', 'round_E', 'round_F', 'round_G', 'round_H',
       'diff_funding_year', 'total_investment']].describe()

cat_invest = pd.cut(df_for_pred_final.total_investment, bins = [-1, 112500, 1400300, 8205200, 40079503000], labels=['low','low_medium','high_medium','high'])
df_for_pred_final.insert(0,'cat_total_investment',cat_invest)

cat_diff_funding_year = pd.cut(df_for_pred_final.diff_funding_year, bins = [-1, 2, 49], labels=['low','high'])
df_for_pred_final.insert(0,'cat_diff_funding_year',cat_diff_funding_year)

cat_funding_rounds = pd.cut(df_for_pred_final.funding_rounds, bins = [-1, 2, 20], labels=['low','high'])
df_for_pred_final.insert(0,'cat_funding_rounds',cat_funding_rounds)

cat_seed = pd.cut(df_for_pred_final.seed, bins = [-1, 28000, 140000000], labels=['low','high'])
df_for_pred_final.insert(0,'cat_seed',cat_seed)

cat_venture = pd.cut(df_for_pred_final.venture, bins = [-1, 85038.5, 6000000, 2451000000], labels=['low','medium','high'])
df_for_pred_final.insert(0,'cat_venture',cat_venture)

df_for_pred_final['cat_status'] = df_for_pred_final['status'].replace(['closed', 'operating', 'acquired'], [0, 1, 2])
df_for_pred_final['cat_total_investment'] = df_for_pred_final['cat_total_investment'].replace(['low','low_medium','high_medium','high'], [0, 1, 2, 3])
df_for_pred_final['cat_diff_funding_year'] = df_for_pred_final['cat_diff_funding_year'].replace(['low', 'high'], [0, 1])
df_for_pred_final['cat_funding_rounds'] = df_for_pred_final['cat_funding_rounds'].replace(['low', 'high'], [0, 1])
df_for_pred_final['cat_seed'] = df_for_pred_final['cat_seed'].replace(['low', 'high'], [0, 1])
df_for_pred_final['cat_venture'] = df_for_pred_final['cat_venture'].replace(['low','medium','high'], [0, 1, 3])

df_for_pred_final.loc[df_for_pred_final['equity_crowdfunding'] < 1, 'cat_equity_crowdfunding'] = 0
df_for_pred_final.loc[df_for_pred_final['equity_crowdfunding'] > 1, 'cat_equity_crowdfunding'] = 1

df_for_pred_final.loc[df_for_pred_final['undisclosed'] < 1, 'cat_undisclosed'] = 0
df_for_pred_final.loc[df_for_pred_final['undisclosed'] > 1, 'cat_undisclosed'] = 1

df_for_pred_final.loc[df_for_pred_final['convertible_note'] < 1, 'cat_convertible_note'] = 0
df_for_pred_final.loc[df_for_pred_final['convertible_note'] > 1, 'cat_convertible_note'] = 1

df_for_pred_final.loc[df_for_pred_final['debt_financing'] < 1, 'cat_debt_financing'] = 0
df_for_pred_final.loc[df_for_pred_final['debt_financing'] > 1, 'cat_debt_financing'] = 1

df_for_pred_final.loc[df_for_pred_final['angel'] < 1, 'cat_angel'] = 0
df_for_pred_final.loc[df_for_pred_final['angel'] > 1, 'cat_angel'] = 1

df_for_pred_final.loc[df_for_pred_final['grant'] < 1, 'cat_grant'] = 0
df_for_pred_final.loc[df_for_pred_final['grant'] > 1, 'cat_grant'] = 1

df_for_pred_final.loc[df_for_pred_final['private_equity'] < 1, 'cat_private_equity'] = 0
df_for_pred_final.loc[df_for_pred_final['private_equity'] > 1, 'cat_private_equity'] = 1

df_for_pred_final.loc[df_for_pred_final['post_ipo_equity'] < 1, 'cat_post_ipo_equity'] = 0
df_for_pred_final.loc[df_for_pred_final['post_ipo_equity'] > 1, 'cat_post_ipo_equity'] = 1

df_for_pred_final.loc[df_for_pred_final['post_ipo_debt'] < 1, 'cat_post_ipo_debt'] = 0
df_for_pred_final.loc[df_for_pred_final['post_ipo_debt'] > 1, 'cat_post_ipo_debt'] = 1

df_for_pred_final.loc[df_for_pred_final['secondary_market'] < 1, 'cat_secondary_market'] = 0
df_for_pred_final.loc[df_for_pred_final['secondary_market'] > 1, 'cat_secondary_market'] = 1

df_for_pred_final.loc[df_for_pred_final['product_crowdfunding'] < 1, 'cat_product_crowdfunding'] = 0
df_for_pred_final.loc[df_for_pred_final['product_crowdfunding'] > 1, 'cat_product_crowdfunding'] = 1

df_for_pred_final.loc[df_for_pred_final['round_A'] < 1, 'cat_round_A'] = 0
df_for_pred_final.loc[df_for_pred_final['round_A'] > 1, 'cat_round_A'] = 1

df_for_pred_final.loc[df_for_pred_final['round_B'] < 1, 'cat_round_B'] = 0
df_for_pred_final.loc[df_for_pred_final['round_B'] > 1, 'cat_round_B'] = 1

df_for_pred_final.loc[df_for_pred_final['round_C'] < 1, 'cat_round_C'] = 0
df_for_pred_final.loc[df_for_pred_final['round_C'] > 1, 'cat_round_C'] = 1

df_for_pred_final.loc[df_for_pred_final['round_D'] < 1, 'cat_round_D'] = 0
df_for_pred_final.loc[df_for_pred_final['round_D'] > 1, 'cat_round_D'] = 1

df_for_pred_final.loc[df_for_pred_final['round_E'] < 1, 'cat_round_E'] = 0
df_for_pred_final.loc[df_for_pred_final['round_E'] > 1, 'cat_round_E'] = 1

df_for_pred_final.loc[df_for_pred_final['round_F'] < 1, 'cat_round_F'] = 0
df_for_pred_final.loc[df_for_pred_final['round_F'] > 1, 'cat_round_F'] = 1

df_for_pred_final.loc[df_for_pred_final['round_G'] < 1, 'cat_round_G'] = 0
df_for_pred_final.loc[df_for_pred_final['round_G'] > 1, 'cat_round_G'] = 1

df_for_pred_final.loc[df_for_pred_final['round_H'] < 1, 'cat_round_H'] = 0
df_for_pred_final.loc[df_for_pred_final['round_H'] > 1, 'cat_round_H'] = 1

labelencoder = LabelEncoder()
df_for_pred_final['cat_country_code'] = labelencoder.fit_transform(df_for_pred_final['country_code'])

df_for_pred_final['cat_industry_group'] = labelencoder.fit_transform(df_for_pred_final['Industry Group'])

df_final = df_for_pred_final[['cat_status', 'cat_industry_group',
       'cat_country_code','cat_funding_rounds',
       'cat_diff_funding_year', 'cat_total_investment' , 
       'cat_equity_crowdfunding', 'cat_venture', 'cat_seed', 'cat_undisclosed',
       'cat_convertible_note', 'cat_debt_financing', 'cat_angel', 'cat_grant',
       'cat_private_equity', 'cat_post_ipo_equity', 'cat_post_ipo_debt',
       'cat_secondary_market', 'cat_product_crowdfunding', 'cat_round_A',
       'cat_round_B', 'cat_round_C', 'cat_round_D', 'cat_round_E',
       'cat_round_F', 'cat_round_G', 'cat_round_H']]

#others are removed which have low values using correlation matrix
df_final_model_1= df_final[['cat_status', 'cat_industry_group', 'cat_country_code',
       'cat_funding_rounds', 'cat_diff_funding_year', 'cat_total_investment', 'cat_venture', 'cat_seed', 'cat_debt_financing', 'cat_angel',
       'cat_private_equity', 'cat_round_A',
       'cat_round_B', 'cat_round_C', 'cat_round_D', 'cat_round_E',
       'cat_round_F']]

y = df_final_model_1.cat_status
X = df_final_model_1.drop(columns=['cat_status'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
model1 = DecisionTreeClassifier(random_state = 100) 
model1 = model1.fit(X_train, y_train)

'''
param_dict = {
    "criterion":['gini', 'entropy'],
    "max_depth": range(1,20),
    "min_samples_split": range(1,20),
    "min_samples_leaf": range(1,10)
}

decision_tree = DecisionTreeClassifier()
grid = GridSearchCV(decision_tree,
                    param_grid = param_dict,
                    cv = 10, # cross validation method
                    verbose = 1,
                    n_jobs = -1) # set to use all processors

grid.fit(X_train, y_train)

grid.best_params_ 

grid.best_estimator_
'''

clf = DecisionTreeClassifier(criterion = 'gini', max_depth = 1, min_samples_leaf = 1, min_samples_split=2, random_state=40)
clf.fit(X_train,y_train) 
'''
sample_data = {'cat_industry_group': np.random.choice(range(0,42,1), size = (5)),
        'cat_country_code': np.random.choice(range(0,112,1), size = (5)),
        'cat_funding_rounds': np.random.choice([0,1], size = (5)),
        'cat_diff_funding_year': np.random.choice([0,1], size = (5)),
        'cat_total_investment': np.random.choice([0,1,2,3], size = (5)),
        'cat_venture': np.random.choice([0,1,2,3], size = (5)),
        'cat_seed': np.random.choice([0,1], size = (5)),
        'cat_debt_financing': np.random.choice([0,1], size = (5)),
        'cat_angel': np.random.choice([0,1], size = (5)),
        'cat_private_equity': np.random.choice([0,1], size = (5)),
        'cat_round_A': np.random.choice([0,1], size = (5)),
        'cat_round_B': np.random.choice([0,1], size = (5)),
        'cat_round_C': np.random.choice([0,1], size = (5)),
        'cat_round_D': np.random.choice([0,1], size = (5)),
        'cat_round_E': np.random.choice([0,1], size = (5)),
        'cat_round_F': np.random.choice([0,1], size = (5))
       }
sample = pd.DataFrame(sample_data, index=[0,1,2,3,4])

ynew = clf.predict(sample)
print(ynew)
'''

pickle.dump(clf,open("model.pkl", "wb"))
