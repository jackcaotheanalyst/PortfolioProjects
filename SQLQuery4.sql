select * 
from PortfolioProject..CovidDeaths
order by 

--select * 
--from PortfolioProject..CovidVaccinations
--order by 3,4

Select location, date, total_cases, new_cases, total_deaths, population
From PortfolioProject..CovidDeaths
Order by 1,2

--looking at the likelihood of dying if infected.
Select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
From PortfolioProject..CovidDeaths
Where location = 'United States'
Order by 1,2

--looking at the infection rate.
Select location, date, total_cases, population, (total_cases/population)*100 as InfectionPercentage
From PortfolioProject..CovidDeaths
Where location = 'United States'
Order by 1,2

--looking at countries with the highest infection rate.
Select location, population, Max(total_cases) as UpToDateInfectionCount, Max(total_cases/population)*100 as InfectionPercentage
From PortfolioProject..CovidDeaths
where continent is not null
Group by location, population
Order by UpToDateInfectionCount desc

--looking at counties with the highest death rate.
Select location, population, Max(cast(total_deaths as int)) as UpToDateDeathCount, Max(cast(total_deaths as int)/population)*100 as DeathPercentage
From PortfolioProject..CovidDeaths
Where continent is not null
Group by location, population
Order by UpToDateDeathCount desc

--looking at continent.
Select location, population, Max(cast(total_deaths as int)) as UpToDateDeathCount, Max(cast(total_deaths as int)/population)*100 as DeathPercentage
From PortfolioProject..CovidDeaths
Where continent is null
Group by location, population
Order by UpToDateDeathCount desc

--looking at global numbers here.
Select date,sum(new_cases) as total_new_cases, sum(convert(int, new_deaths)) as total_new_deaths, (sum(convert(int, new_deaths))/sum(new_cases))*100 as DailyDeathPercentage
From PortfolioProject..CovidDeaths
Where continent is not null
Group by date
Order by date

--looking at the vaccinations.
Select dea.continent, dea.location, dea.population, vac.new_vaccinations
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not null
	and dea.location = 'United States'
Order by 2, 3

--looking at the rolling number.
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
	Sum(convert(int, vac.new_vaccinations)) Over (Partition by dea.location Order by dea.location, dea.date) as RollingVaccineCount
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not null
Order by 2, 3

--CTE
With PopvsVac (continent, location, date, population, new_vaccinations, RollingVaccinatedCount)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
	Sum(convert(int, vac.new_vaccinations)) Over (Partition by dea.location Order by dea.location, dea.date) as RollingVaccinatedCount
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not null
)
Select *, (RollingVaccinatedCount/population)*100 as RollingVaccinatedRate
From PopvsVac
Where location = 'United States'

--Temp Table
Drop Table if exists PopvsVac
Create Table PopvsVac
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population float,
New_Vaccinations float,
RollingVaccinatedCount float
)
Insert into PopvsVac
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
	Sum(convert(int, vac.new_vaccinations)) Over (Partition by dea.location Order by dea.location, dea.date) as RollingVaccinatedCount
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not null
Select *, (RollingVaccinatedCount/population)*100 as RollingVaccinatedRate
From PopvsVac
Where location = 'United States'

--Creating views
Create View RatePeopleVaccinated as
With PopvsVac (continent, location, date, population, new_vaccinations, RollingVaccinatedCount)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
	Sum(convert(int, vac.new_vaccinations)) Over (Partition by dea.location Order by dea.location, dea.date) as RollingVaccinatedCount
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not null
)
Select *, (RollingVaccinatedCount/population)*100 as RollingVaccinatedRate
From PopvsVac

Select *
From RatePeopleVaccinated
Where location = 'United States'