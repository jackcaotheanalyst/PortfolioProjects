Select *
From PortfolioProject..NashvilleHousing

Select SaleDate, Convert(Date, SaleDate)
From PortfolioProject..NashvilleHousing

Update PortfolioProject..NashvilleHousing
Set SaleDate = Convert(Date, SaleDate)

Alter Table PortfolioProject..NashvilleHousing
Add SaleDateConverted Date;

Update PortfolioProject..NashvilleHousing
Set SaleDateConverted = Convert(date, SaleDate)

--Update the null value on some of the obs' propery addresses.
Select *
From PortfolioProject..NashvilleHousing
--Where PropertyAddress is null
Order by ParcelID

Select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, Isnull(a.PropertyAddress, b.PropertyAddress)
From PortfolioProject..NashvilleHousing a
Join PortfolioProject..NashvilleHousing b 
	On a.ParcelId = b.ParcelID
	And a.[UniqueID ] <> b.[UniqueID ]
Where a.PropertyAddress is null

Update a
Set PropertyAddress = Isnull(a.PropertyAddress, b.PropertyAddress)
From PortfolioProject..NashvilleHousing a
Join PortfolioProject..NashvilleHousing b
	On a.ParcelID = b.ParcelID
	And a.[UniqueID ] <> b.[UniqueID ]
Where a.PropertyAddress is Null

--Breaking out address into individual coloums (Address, City, State)
Select *
From PortfolioProject..NashvilleHousing


Select Substring(PropertyAddress, 1, Charindex(',', PropertyAddress) - 1) as Address, 
	Substring(PropertyAddress, Charindex(',', PropertyAddress) + 1, Len(PropertyAddress)) as City
From PortfolioProject..NashvilleHousing

Alter Table PortfolioProject..NashvilleHousing
Add Property_Address Nvarchar(255);

Update PortfolioProject..NashvilleHousing
Set Property_Address = Substring(PropertyAddress, 1, Charindex(',', PropertyAddress) - 1)

Alter Table PortfolioProject..NashvilleHousing
Add Property_City Nvarchar(255);

Update PortfolioProject..NashvilleHousing
Set Property_City = Substring(PropertyAddress, Charindex(',', PropertyAddress) + 1, Len(PropertyAddress))

--
Select *
From PortfolioProject..NashvilleHousing

Select Parsename(Replace(OwnerAddress, ',', '.'), 3) as Address,
	Parsename(Replace(OwnerAddress, ',', '.'), 2) as City,
	Parsename(Replace(OwnerAddress, ',', '.'), 1) as State
From PortfolioProject..NashvilleHousing

Alter Table PortfolioProject..NashvilleHousing
Add Owner_Address Nvarchar(255), Owner_City Nvarchar(255), Owner_State Nvarchar(255);

Update PortfolioProject..NashvilleHousing
Set Owner_Address = Parsename(Replace(OwnerAddress, ',', '.'), 3),
	Owner_City = Parsename(Replace(OwnerAddress, ',', '.'), 2),
	Owner_State = Parsename(Replace(OwnerAddress, ',', '.'), 1);

--Change Y and N to Yes and No
Select Distinct(SoldAsVacant), Count(SoldAsVacant)
From PortfolioProject..NashvilleHousing
Group by SoldAsVacant
Order by 2

Select SoldAsVacant,
	Case When SoldAsVacant = 'Y' Then 'Yes'
		When SoldAsVacant = 'N' Then 'No'
		Else SoldAsVacant
		End
From PortfolioProject..NashvilleHousing

Update PortfolioProject..NashvilleHousing
Set SoldAsVacant = Case When SoldAsVacant = 'Y' Then 'Yes'
						When SoldAsVacant = 'N' Then 'No'
						Else SoldAsVacant
						End

--Remove Duplicates
With RownumCTE as (
Select *, 
	Row_number() Over (
	Partition by ParcelID,
				PropertyAddress,
				SalePrice,
				SaleDate,
				LegalReference
				Order by 
					UniqueID
					) row_num
From PortfolioProject..NashvilleHousing
--Order by ParcelID
)
Delete 
From RownumCTE
Where row_num > 1

--Select *
--From RownumCTE
--Where row_num > 1
--Order by PropertyAddress

--Delete unused column
Select *
From PortfolioProject..NashvilleHousing

Alter Table PortfolioProject..NashvilleHousing
Drop Column OwnerAddress, TaxDistrict, PropertyAddress, SaleDate
