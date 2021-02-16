CREATE DATABASE IF NOT EXISTS alpacastack;
USE alpacastack;

CREATE TABLE `alpacastack`.`assets` (
  `id` VARCHAR(100) NOT NULL,
  `class` VARCHAR(45) NOT NULL,
  `exchange` VARCHAR(45) NOT NULL,
  `symbol` VARCHAR(5) NOT NULL,
  `tradable` BIT(1) NOT NULL,
  `marginable` BIT(1) NOT NULL,
  `shortable` BIT(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC));

CREATE TABLE `alpacastack`.`positions` (
  `id` VARCHAR(100) NOT NULL,
  `asset_id` VARCHAR(100) NOT NULL,
  `symbol` VARCHAR(5) NOT NULL,
  `exchange` VARCHAR(45) NOT NULL,
  `avg_entry_price` DECIMAL(5,5) NOT NULL,
  `qty` INT NOT NULL,
  `side` VARCHAR(5) NOT NULL,
  `market_value` DECIMAL(5,5) NOT NULL,
  `cost_basis` DECIMAL(5,5) NOT NULL,
  `unrealized_pl` DECIMAL(5,5) NOT NULL,
  `unrealized_plpc` DECIMAL(5,5) NOT NULL,
  `unrealized_intraday_pl` DECIMAL(5,5) NOT NULL,
  `unrealized_intraday_plpc` DECIMAL(5,5) NOT NULL,
  `current_price` DECIMAL(5,5) NOT NULL,
  `lastday_price` DECIMAL(5,5) NOT NULL,
  `change_today` DECIMAL(5,5) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC));